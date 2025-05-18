import glob
import mmh3
import os


class CCalignerAlgorithm:
    def __init__(self, codeblocks_dir, lang_ext, window_size=3, edit_distance=1, theta=0.7, query_file=None):
        if not query_file:
            raise ValueError("Parameter query_file is mandatory.")
        if not os.path.isfile(query_file):
            raise FileNotFoundError(f"Query file not found: {query_file}")

        self.dir = codeblocks_dir
        self.q = window_size
        self.e = edit_distance
        self.theta = theta
        self.query_file = query_file

        self.files = []
        for file in glob.glob(self.dir + "/**/*" + lang_ext, recursive=True):
            self.files.append(file)

        self.cand_map = dict()
        self.hash_set = dict()
        self.cand_pair = set()
        self.clone_pair = []

    @staticmethod
    def all_combinations(arr: list, k: int) -> list:
        n = len(arr)

        def complete_combination(start, combination):
            if len(combination) == k:
                combinations.append(combination[:])
                return
            for i in range(start, n):
                combination.append(arr[i])
                complete_combination(i + 1, combination)
                combination.pop()

        combinations = []
        complete_combination(0, [])
        return combinations

    def index_codeblock(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
        L = len(lines)
        num_of_wndws = L - self.q + 1
        hash_sub_set = set()
        for win_start in range(num_of_wndws):
            window = lines[win_start : win_start + self.q]
            for h in self.all_combinations(window, self.q - self.e):
                k = mmh3.hash128("".join(h))
                hash_sub_set.add(str(k) + '|' + str(win_start))
                if k in self.cand_map:
                    self.cand_map[k].add(file)
                else:
                    self.cand_map[k] = {file}
        self.hash_set[file] = hash_sub_set

    def verify_pairs(self):
        for f_m_f_n in self.cand_pair:
            f_m, f_n = f_m_f_n.split('|')
            hashes_in_f_m = set(hash_pair.split('|')[0] for hash_pair in self.hash_set[f_m])
            hashes_in_f_n = set(hash_pair.split('|')[0] for hash_pair in self.hash_set[f_n])
            hashes_intersection = hashes_in_f_n.intersection(hashes_in_f_m)
            num_match_1 = len(
                set(hash_pair.split('|')[1] for hash_pair in self.hash_set[f_m] if hash_pair.split('|')[0] in hashes_intersection))
            num_match_2 = len(
                set(hash_pair.split('|')[1] for hash_pair in self.hash_set[f_m] if hash_pair.split('|')[0] in hashes_intersection))

            num_win_m = sum(1 for _ in open(f_m)) - self.q + 1
            num_win_n = sum(1 for _ in open(f_n)) - self.q + 1
            if num_match_1 >= self.theta * num_win_m or num_match_2 >= self.theta * num_win_n:
                self.clone_pair.append([f_m, f_n])

    def run_algo(self):
        for file in self.files:
            self.index_codeblock(file)

        self.index_codeblock(self.query_file)

        for mapp in self.cand_map.values():
            if len(mapp) >= 2:
                hashable_pairs = []
                for pair in self.all_combinations(list(mapp), 2):
                    if (pair[0] == self.query_file) or (pair[1] == self.query_file):
                        hashable_pairs.append(pair[0] + '|' + pair[1])
                self.cand_pair.update(hashable_pairs)
        self.verify_pairs()

        return self.clone_pair
