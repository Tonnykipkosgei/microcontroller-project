from machine import I2S, Pin

# Define constants
WAV_FILE = 'taunt.wav'        # Path to the WAV file
SAMPLE_RATE_IN_HZ = 22300      # Sample rate of the audio
bits_per_sample = 8            # Number of bits per audio sample

# Pins configuration for I2S
bck_pin = Pin(33)              # Bit clock pin
ws_pin = Pin(25)               # Word select pin
sdout_pin = Pin(32)            # Data out pin

# Initialize the I2S audio output
audio_out = I2S(
                # I2S peripheral number (0 or 1)
                0,
                
                # Bit clock pin
                sck=bck_pin,
                
                # Word select pin
                ws=ws_pin,
                
                # Data out pin
                sd=sdout_pin,
                
                # Set as a transmitter
                mode=I2S.TX,
                
                # Number of bits per sample
                bits=8,
                
                # Mono audio format
                format=I2S.MONO,

                # Sample rate
                samplerate=SAMPLE_RATE_IN_HZ,

                # Internal buffer size
                ibuf=20000)


# Open the WAV file in read-binary mode
wav = open(WAV_FILE, 'rb')

# Seek to the start of the data section in the WAV file
pos = wav.seek(44)  

# Allocate memory for storing audio samples
wav_samples = bytearray(2048)

wav_samples_mv = memoryview(wav_samples)

print('Test: This is the starting point')

# Main loop for continuously playing audio
while True:
    try:
        # Read audio samples from the WAV file into the buffer
        num_read = wav.readinto(wav_samples_mv)
        num_written = 0
        
        # If all samples are read, reset to the start of the data section
        if num_read == 0:
            pos = wav.seek(44)
        else:
            # Write audio samples to the I2S peripheral
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read], timeout=0)
    except (KeyboardInterrupt, Exception) as e:
        # Exception handling
        print('Caught exception {} {}'.format(type(e).__name__, e))
        break

# Close the WAV file
wav.close()

# Deinitialize the audio output
audio_out.deinit()

print('Done')
