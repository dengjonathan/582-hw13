#!/usr/bin/env python3
import random

try:
        from params import p
        from params import g
except ImportError:
        raise ImportError("Could not import parameter file 'params.py'")

def validate():
    try:
        import elgamal
    except ImportError:
        raise ImportError("Could not import homework file 'elgamal.py'")
        return 0        

    required_methods = ["encrypt","decrypt"]
    for m in required_methods:
        if m not in dir(elgamal):
            print( "%s not defined"%m )
            return 0

    num_tests = 5

    num_passed = 0
    for _ in range(num_tests):
        try:
            pk,sk = elgamal.keygen()
        except Exception as e:
            print( "ERROR: keygen failed" )
            continue
        print( "Key generation ran" )
        m = random.SystemRandom().randint(1,p//2)
        try:
            c = elgamal.encrypt(pk,m)
        except Exception as e:
            print( "ERROR: encrypt failed" )
            continue
        print( "Encrypt ran without exceptions" )
        try:
            m2 = elgamal.decrypt(sk,c)
        except Exception as e:
            print( "ERROR: decrypt failed with exception" )
            continue
        print( "decrypt ran" )
        if m == m2: #Did decryption succeed
            print( "decryption succeeded" )
            num_passed = num_passed + 1
        else: 
            print( "Decryption failed to undo encryption" )

    print( f"Passed {num_passed}/{num_tests}" )
    return num_passed * (100 / num_tests)
