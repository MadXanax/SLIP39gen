from shamir_mnemonic import shamir
from mnemonic import Mnemonic
from cryptography.hazmat.primitives import constant_time
import ctypes
import gc

def validate_seed_phrase(seed_phrase):
    """
    Validate the BIP39 seed phrase to ensure it is correct.
    """
    mnemo = Mnemonic("english")
    if not mnemo.check(seed_phrase):
        print()
        raise ValueError("Invalid seed phrase. Please ensure it is a valid BIP39 24-word seed phrase.\n\n=================== END 1 ===================\n")
    return seed_phrase

def get_entropy_from_seed_phrase(seed_phrase):
    """
    Convert the BIP39 seed phrase to entropy (256-bit).
    """
    mnemo = Mnemonic("english")
    try:
        entropy = mnemo.to_entropy(seed_phrase)
    except ValueError as e:
        print()
        raise ValueError(f"Error converting seed phrase to entropy: {e}\n\n=================== END 2 ===================\n")
    
    # Ensure entropy is 256 bits (32 bytes)
    if len(entropy) != 32:
        print()
        raise ValueError("Entropy must be 256 bits (32 bytes). Please check your seed phrase.\n\n=================== END 3 ===================\n")
    
    return entropy

def get_user_seed_phrase():
    """
    Get and confirm the BIP39 seed phrase from the user.
    """
    print("\n=================== START ===================")
    seed_phrase = input("\n Enter your BIP39 seed phrase (24 words):\n")
    confirm_seed_phrase = input("\n Please re-enter your BIP39 seed phrase to confirm:\n")
    
    if seed_phrase != confirm_seed_phrase:
        print()
        raise ValueError("The seed phrases do not match. Please try again.\n\n=================== END 4 ===================\n")

    return seed_phrase

def get_user_input():
    """
    Get user input for Shamir Secret Sharing configuration.
    """
    # Get and confirm the seed phrase
    seed_phrase = get_user_seed_phrase()

    # Validate seed phrase
    seed_phrase = validate_seed_phrase(seed_phrase)

    # Convert seed phrase to entropy
    entropy = get_entropy_from_seed_phrase(seed_phrase)

    # Ask for a passphrase (optional)
    passphrase = input("\nEnter a secret-passphrase for additional security (not recommanded, leave empty if not needed): ")
    passphrase_bytes = passphrase.encode('utf-8')

    # Hardcoded values for group configuration
    num_groups = 1
    group_threshold = 1




    group_counts = []
    for i in range(num_groups):
        member_threshold = int(input(f"\nEnter the member THRESHOLD for group {i + 1} (min. shares required to reconstruct): "))
        num_shares = int(input(f"Enter the TOTAL number of SHARES for group {i + 1}: "))

        # Validate user input
        if member_threshold > num_shares:
            print()
            raise ValueError(f"Member threshold cannot exceed the total number of shares for group {i + 1}.\n\n=================== END 5 ===================\n")
        
        group_counts.append((member_threshold, num_shares))

    # We no longer check group_threshold against num_groups since both are hardcoded to 1

    return entropy, group_threshold, group_counts, passphrase_bytes




def secure_delete(variable):
    """
    Overwrite and delete sensitive data in memory to reduce exposure risk.
    """
    if isinstance(variable, str):
        buffer = ctypes.create_string_buffer(len(variable))
        ctypes.memset(ctypes.addressof(buffer), 0, len(variable))
        constant_time.bytes_eq(buffer.raw, b'\x00' * len(variable))
    elif isinstance(variable, list):
        for i in range(len(variable)):
            if isinstance(variable[i], str):
                buffer = ctypes.create_string_buffer(len(variable[i]))
                ctypes.memset(ctypes.addressof(buffer), 0, len(variable[i]))
                constant_time.bytes_eq(buffer.raw, b'\x00' * len(variable[i]))
            variable[i] = None
    gc.collect()

def generate_shamir_shares(entropy, group_threshold, group_counts, passphrase):
    """
    Generate SLIP39 mnemonic shares using the provided entropy, configuration, and passphrase.
    """
    try:
        mnemonic_shares = shamir.generate_mnemonics(group_threshold, group_counts, entropy, passphrase=passphrase)
    except Exception as e:
        print()
        raise RuntimeError(f"Error generating mnemonic shares: {e}\n\n=================== END 7 ===================\n")
    
    return mnemonic_shares

def display_mnemonic_shares(mnemonic_shares):
    """
    Display the generated SLIP39 mnemonic shares to the user.
    """
    print()
    print("=============================================")
    print("\nYour mnemonic shares:")
    print()
    num_groups = len(mnemonic_shares)  # Determine the number of groups
    for i, group in enumerate(mnemonic_shares):
        print(f" Group {i + 1}:\n")
        for j, share in enumerate(group):
            print(f"  Share {j + 1}:\n{share}")
            print()
        # Print separator only if there are more than one group and not the last group
        if num_groups > 1 and i < num_groups - 1:
            print("---------------------------------------------")
            print()
    print("=================== END N ===================\n")  # Print only after the last group

def main():
    try:
        # Step 1: Get user input and validate
        entropy, group_threshold, group_counts, passphrase = get_user_input()

        # Step 2: Generate SLIP39 mnemonic shares
        mnemonic_shares = generate_shamir_shares(entropy, group_threshold, group_counts, passphrase)

        # Step 3: Display the mnemonic shares
        display_mnemonic_shares(mnemonic_shares)

        # Securely delete sensitive data after use
        secure_delete(entropy)
        secure_delete(passphrase)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
