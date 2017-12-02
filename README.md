# cputhief-backend

How to talk to this API:

1. Send a GET request to the /api/get_number endpoint.

2. You will receive a JSON with 2 values, "block" and "n".

  block: start checking for primes from this number
  
  n: check n numbers

3. Check all the numbers in the interval [block, block + n]. 

4. Create a JSON with the values "result" (a list containing all primes you found), and "block" and "n" (the original ones you got from the API)

5. Send this JSON to the /api/post_results endpoint.

5. Repeat :)
