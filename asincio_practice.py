import asyncio


async def square_number(number):
    pass


async def parallel_execution(numbers):
    pass


numbers = [int(i) for i in input().split()]
results = asyncio.run(parallel_execution(numbers))
print(*results)
