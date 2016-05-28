from MMM import Speaker
import sys
import time

# Create a speaker
speaker = Speaker();
raw_input("Press Enter.") 

# Say something!
speaker.speak("Good day sir.")
time.sleep(5.0)

# Say something else!
speaker.speak("How are you doing?")
time.sleep(5.0)

# Say one more thing!
speaker.speak("I am doing just fine thank you very much.")
time.sleep(5.0)

# End connection
speaker.osc.close()
mmm.ser.close()
quit()
