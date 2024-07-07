
import hashlib

class MerkleNode:
    def __init__(self, left=None, right=None, hash_value=None, data=None):
        self.left = left
        self.right = right
        self.hash_value = hash_value
        self.data = data

    def calculate_hash(self):
        if self.data is not None:
            # 如果是叶子节点，直接计算数据的哈希值
            self.hash_value = hashlib.sha256(self.data.encode()).hexdigest()
        else:
            # 否则，计算左右子节点哈希值的串联后的哈希值
            combined_hash = self.left.hash_value + self.right.hash_value
            self.hash_value = hashlib.sha256(combined_hash.encode()).hexdigest()

    def __repr__(self):
        return f"MerkleNode(hash_value={self.hash_value})"

def build_merkle_tree(data_blocks):
    if len(data_blocks) == 0:
        return None

        # 递归构建默克尔树
    if len(data_blocks) % 2 == 1:
        # 如果数据块数量为奇数，复制最后一个数据块
        data_blocks.append(data_blocks[-1])

    nodes = [MerkleNode(data=block) for block in data_blocks]

    while len(nodes) > 1:
        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else left.copy()  # 复制节点以处理奇数情况
            combined = MerkleNode(left, right)
            combined.calculate_hash()
            new_level.append(combined)
        nodes = new_level

    return nodes[0]  # 返回根节点

def verify_merkle_proof(root, leaf, proof):
    # 验证从根到叶子的路径（proof）
    node = root
    for index, hash_value in enumerate(proof):
        if index % 2 == 0:  # 假设proof中的偶数索引是左子节点的哈希
            if hash_value != node.left.hash_value:
                return False
            node = node.right
        else:  # 奇数索引是右子节点的哈希
            if hash_value != node.right.hash_value:
                return False
            node = node.left

            # 最后检查叶子节点的哈希值
    return leaf.hash_value == node.hash_value

# 示例用法
data_blocks = ["block1", "block2", "block3", "block4"]
root = build_merkle_tree(data_blocks)
print("Root hash:", root.hash_value)

# 假设我们要验证"block3"
leaf = MerkleNode(data="block3")
leaf.calculate_hash()

# 这里需要手动生成或从某处获取proof，这里仅作为示例
# 假设proof是[root.left.hash_value, root.right.left.hash_value]
# 注意：这通常不是由用户手动完成的，而是由系统提供的
proof = [root.left.hash_value, root.right.left.hash_value]

if verify_merkle_proof(root, leaf, proof):
    print("Verification successful!")
else:
    print("Verification failed!")