# write an async function that 
# simulates fetching data from two different agent tools concurrently using asyncio.gather().

import asyncio
import time
import random 
from datetime import datetime

async def today_time():

    print("Fetching today's time...")
    await asyncio.sleep(2)  # Non-blocking pause for 2 seconds
    
    #current_time = time.strftime("%X")

    current_time = datetime.now().strftime("%X")
    
    print(f"The current time is: {current_time}")

    return current_time

async def proverb():
    warrior_proverbs = [
    "The two most powerful warriors are patience and time.",
    "He who conquers himself is the mightiest warrior.",
    "The more you sweat in training, the less you bleed in battle.",
    "Every victorious warrior is a self-made one.",
    "A warrior accepts that he is not in control of everything, but controls his spirit."
    ]

    print("Fetching today's proverb...")
    selected_proverb = random.choice(warrior_proverbs)
    print(f"Today's proverb is: {selected_proverb}")
    return selected_proverb


async def main():
    # Unpack the returned results from both tools
    current_time, proverb_text = await asyncio.gather(today_time(), proverb())
    
    print("\n--- Agent Summary ---")
    print(f"Executed at: {current_time}")
    print(f"Thought for the day: {proverb_text}")

asyncio.run(main())

""" what we learned is that 
keyword for asynchronized function is - async 
its good for I/O Bound work that is the work that depends upon network and input output through the network 
not good for cpu bound which is the heavy lifting math generating etc we use multithreading for that
asyncio.sleep(2) means sleep for 2 but other system will ofcourse work its opposite of time.sleep(2)
"""