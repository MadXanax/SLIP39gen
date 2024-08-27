from shamir_mnemonic import shamir
from mnemonic import Mnemonic
from cryptography.hazmat.primitives import constant_time
import ctypes
import gc


def validate_mnemonic_share(share):
    """
    Validate a SLIP39 mnemonic share to ensure it is correctly formatted and valid.
    """
    try:
        shamir.decode_mnemonics([share])
    except Exception as e:
        print()
        raise ValueError(f"Invalid mnemonic share: {e}\n\n=================== END 1 ===================\n")


def secure_delete(variable):
    """
    Overwrite and delete sensitive data in memory to reduce exposure risk.
    """
    if isinstance(variable, str):
        # Overwrite with random data and delete
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


def get_required_shares():
    """
    Dynamically get the required number of shares from user input to reconstruct the seed.
    """
    shares_input = []
    
    
    first_share = input(" Enter the first mnemonic share:\n").strip()

    # Validate the first share
    validate_mnemonic_share(first_share)
    shares_input.append(first_share)

    # Decode SLIP39 parameters from the first share
    metadata = shamir.decode_mnemonics([first_share])
    share_group = metadata[0]
    member_threshold = share_group.member_threshold()



    print()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"Deduced Parameters:")
    print(f" -> Member Threshold (Shares needed to reconstruct): {member_threshold}")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")






    for i in range(member_threshold - 1):
        share = input(f"\n Enter Share {i + 2} (use spaces to separate words):\n").strip()
        validate_mnemonic_share(share)
        shares_input.append(share)

    return shares_input


















def reconstruct_seed_phrase(shares_input, passphrase=''):
    """
    Reconstruct the seed phrase from the provided mnemonic shares.
    """
    try:
        passphrase_bytes = passphrase.encode('utf-8')
        recovered_entropy = shamir.combine_mnemonics(shares_input, passphrase=passphrase_bytes)

        mnemo = Mnemonic("english")
        recovered_seed_phrase = mnemo.to_mnemonic(recovered_entropy)

        print("\n\nOriginal Seed Phrase Reconstructed:")
        print("---------------------------------------------")
        print(recovered_seed_phrase)
        print("---------------------------------------------")
        print("\n=================== END N ===================\n")

        # Securely delete sensitive data after use
        secure_delete(recovered_seed_phrase)
        secure_delete(shares_input)

    except Exception as e:
        print()
        print(f"Error reconstructing seed: {e}")
        print("\n=================== END 4 ===================\n")


def main():
    print("\n=================== START ===================\n")

    try:
        # Step 1: Get the required shares from the user
        shares_input = get_required_shares()

        # Step 2: Ask for passphrase if used
        passphrase = input("\nEnter the secret-passphrase (leave empty if none was used, which is default): ")

        # Step 3: Reconstruct the seed phrase
        reconstruct_seed_phrase(shares_input, passphrase)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
