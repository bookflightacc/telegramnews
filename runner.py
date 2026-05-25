import asyncio
import time
from main import main

while True:

    try:
        asyncio.run(main())

    except Exception as e:
        print("RUNNER ERROR:", e)

    # wait 30 mins
    time.sleep(1800)