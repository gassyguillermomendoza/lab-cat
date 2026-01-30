'''
BAD IMPLEMENTATION: O(n) memory complexity
This version reads the ENTIRE input into memory before writing any output.
For an infinite stream like /dev/urandom, this will consume unbounded memory
until the system runs out of RAM and the process is killed (OOM).

Why O(n): The read() call without a size argument accumulates ALL input bytes
into a single Python bytes object. If input is n bytes, memory usage is O(n).

Why this is bad:
1. Cannot process infinite streams (like /dev/urandom, pipes, network sockets)
2. Will crash on files larger than available RAM
3. High latency: no output until entire input is consumed
4. Wasteful: cat only needs to hold one chunk at a time, not everything
'''
import sys

def cat(file):
    # BUG: read() with no argument reads until EOF, storing everything in memory
    data = file.read()  # <-- This is the O(n) memory bug
    sys.stdout.buffer.write(data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            with open(filename, "rb") as f:
                cat(f)
    else:
        # When stdin is an infinite stream, this never returns and grows forever
        cat(sys.stdin.buffer)
