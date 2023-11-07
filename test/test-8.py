import hashlib

def compare_sha256(file_path, given_sha256):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        computed_sha256 = sha256_hash.hexdigest()

    if computed_sha256 == given_sha256:
        return "The SHA256 match"
    else:
        return "The SHA256 hashes do not match"

# Test the function
file_path = "D:/AI/llama.cpp/models/deepseek-coder-6.7b-instruct.Q5_K_M.gguf"
given_sha256 = "0976ee1707fc97b142d7266a9a501893ea6f320e8a8227aa1f04bcab74a5f556"
print(compare_sha256(file_path, given_sha256))