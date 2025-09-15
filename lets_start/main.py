import time
time.sleep(0.1) # Wait for USB to become ready

print( "\n".join( str(n) for n in range(10) ) )

print( "You are Superman!"
    if input("What is your name? ").lower() == "superman"
    else "You are an ordinary person." )