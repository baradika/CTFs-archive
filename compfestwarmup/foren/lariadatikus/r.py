def main():
    p_high = 5806406398969384014051401943911934473343856601864501758929
    q_low = 204145888726158943712172562096470320803814241422555164408967051621495770720517686918929
    n = 1307769497987713293875319341071861744412591449874415928299997687625533629206106982666459858394794273554226098013238158328352186578432689007768548261304019131117056968642157766787344879790233500769614091770191616364020926638224879867
    enc_flag = 1230976585703949844318678047614923087806521813843206194860093242371597417360289806989753007253098864665501116364145242636580717950174995335584680285657026494372820012375639226383052124097330286879695993918743874244364689950316377573

    # Bit lengths and shifts
    total_bits = 768
    known_q_bits = 288  # Lower bits of q
    shift = total_bits - 96  # 768 - 96 = 672 bits to shift to get top 96 bits of n

    # Calculate top 96 bits of n
    n_high = n >> shift

    # Try possible carry values (0 to 3)
    for carry in range(4):
        T_high = n_high - carry
        if T_high < 0:
            continue
        
        # Calculate bounds for q_high
        num_low = T_high * (1 << 192)
        num_high = (T_high + 1) * (1 << 192) - 1
        
        low_bound = (num_low + p_high - 1) // p_high  # Ceiling division
        high_bound = num_high // p_high  # Floor division
        
        # Iterate over possible q_high values
        for q_high in range(low_bound, high_bound + 1):
            # Ensure q_high is 96 bits
            if q_high < 0 or q_high >= (1 << 96):
                continue
                
            # Reconstruct q
            q = (q_high << known_q_bits) + q_low
            if q == 0:
                continue
                
            # Check if q divides n
            if n % q == 0:
                p = n // q
                # Ensure p and q are correct
                if p * q == n:
                    # Decrypt the flag
                    e = 65537
                    phi = (p - 1) * (q - 1)
                    d = pow(e, -1, phi)
                    flag_int = pow(enc_flag, d, n)
                    flag_bytes = long_to_bytes(flag_int)
                    print(flag_bytes.decode())
                    return
                    
    print("Failed to factorize n")

def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

if __name__ == "__main__":
    main()
