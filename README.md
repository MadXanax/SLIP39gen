# SLIP39gen
A Python tool to split a BIP39 24-word seed phrase into Shamir Secret Shares (SLIP39) for enhanced security and backup.


Welcome to the SLIP39gen repository! This project provides a Python-based tool to split a BIP39 24-word seed phrase into multiple mnemonic shares using the Shamir Secret Sharing scheme (SLIP39). This enhances the security and redundancy of your cryptocurrency backups, ensuring that your sensitive seed phrase can be securely stored and reconstructed when needed.

Features
--------
Seed Phrase Validation: Checks the validity of a 24-word BIP39 seed phrase to ensure it's correctly formatted and adheres to the standard.
Entropy Conversion: Converts the validated seed phrase into 256-bit entropy, a prerequisite for generating mnemonic shares.
Shamir Secret Sharing: Uses the SLIP39 protocol to split the seed phrase entropy into multiple mnemonic shares, each of which can be used to reconstruct the original seed phrase when combined.
Secure Data Handling: Implements secure deletion of sensitive data from memory after use to minimize the risk of exposure.
User-Friendly Interface: Command-line interface for easy interaction, allowing users to input their seed phrase and customize the Shamir Secret Sharing configuration.

Installation
------------
Clone the repository:

    git clone https://github.com/yourusername/shamir-seed-splitter.git

Navigate to the project directory:

    cd shamir-seed-splitter

Install required dependencies: Ensure you have Python 3.6+ installed. Install the necessary libraries:

    pip install -r requirements.txt

Usage
-----
Run the script Split_Seedphrase_into_ShmairShares.py
Follow the prompts to enter your 24-word BIP39 seed phrase. You'll be asked to confirm the phrase for accuracy.
Configure the Shamir Secret Sharing settings. Input the member threshold and total number of shares for each group.

Generate Mnemonic Shares: The tool will create mnemonic shares that can be stored separately for secure backup.

Securely Delete Data: Once the shares are generated, the script securely deletes sensitive data from memory.

Example
Upon running the script, you'll see prompts like:

    Enter your BIP39 seed phrase (24 words):
    Please re-enter your BIP39 seed phrase to confirm:
    Enter the member THRESHOLD for group 1 (min. shares required to reconstruct):
    Enter the TOTAL number of SHARES for group 1:
    ...
    Your mnemonic shares:
     Group 1:
       Share 1: [Share mnemonic words]
       Share 2: [Share mnemonic words]
    ...

Security Considerations
-----------------------
Secure Deletion: The tool uses a custom secure delete function to clear sensitive data from memory after use. However, it is recommended to run the script on a secure, offline environment to minimize risks, like an air-gapped computer.

Passphrase Protection: Users have the option to add an extra passphrase to enhance the security of their shares. Proceed at your own risk. Might be imcompatible with hardware/software wallets recovery process.

Contributing
------------
Contributions are welcome! Please fork this repository and open a pull request to contribute to the project. If you have any feature requests or found any bugs, feel free to open an issue.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------
This project is inspired by the Shamir Secret Sharing implementation in Trezor hardware wallets, providing a software-based alternative for secure seed phrase backup.

Limitations
-----------
* The tool is only compatible with a group number of 1, as of now
