def greatest_common_divisor(a:int,b:int):
    """One way to find the GCD of two numbers is based on the observation that if r is the remainder when a is divided by b, 
    then gcd(a, b) = gcd(b, r). As a base case, we can use gcd(a, 0) = a.
    """
    #take and store the smaller value between a and b in i, and the greater value in x
    i = max(a,b)
    x = min(a,b)
    #take and store the remainder of i / x
    r = i % x
    #if the remainder is 0, then you are at the base case and return x.
    if r == 0:
        #print('here1>>', "breakpoint a == 0 or b ==0")
        return x
    else:
        #print(i,x,r)
        #print(greatest_common_divisor(x, r))
        #call function recursively based on algorithm that was provided
        return greatest_common_divisor(x, r)

        

print(greatest_common_divisor(8112,28))
