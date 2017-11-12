import random
import mmh3
import time
import sys


def random_hash_seeds(size, rand_seed=5):
    random.seed(rand_seed)
    return random.sample(range(1, size + 1), size)


def compare_sets(setA, setB):
    return len(setA.intersection(setB)) / len(setA.union(setB))


class Shingling:
    def __init__(self, filename, shingle_length=5):
        print("Shingling Initiated for Doc: %s" % filename)
        with open(filename, 'r') as content_file:
            text = content_file.read()

        t0 = time.time()
        split_text = text.split()
        if len(split_text) < shingle_length:
            print("Text length is less than the length of shingle")
        self.shingles = []
        for shingle in [text[i:i + shingle_length] for i in
                        range(len(text) - shingle_length + 1)]:  # Computing K shingle Here
            self.shingles.append(shingle)

        print("Shingling Ended for doc : %s Time Taken: %.2f sec." % (filename, time.time() - t0))

        t0 = time.time()
        self.minHashObj = MinHashing(self.shingles)
        print("MinHashing Ended for doc : %s Time Taken: %.2f sec." % (filename, time.time() - t0))
        self.computed_MinHash = self.minHashObj.get_MinHash()

    def similarity(self, target_shingled_text):
        return compare_sets(set(self.computed_MinHash), set(target_shingled_text.computed_MinHash))


class MinHashing:
    def __init__(self, Shingles, minhash_size=100, random_seed=5):
        self.minhash = []
        for HASH_SEED in random_hash_seeds(minhash_size, random_seed):
            minimum_val = float('inf')
            for shingle in Shingles:
                hashed_value = mmh3.hash(' '.join(shingle), HASH_SEED)
                minimum_val = min(minimum_val, hashed_value)
            self.minhash.append(minimum_val)

    def get_MinHash(self):
        return self.minhash


class CompareDocs:
    def __init__(self, database, Shingle_len, MinHash_size, Similarity_thresHOld):

        self.DocList = []
        self.DocObj = []
        self.shingle_length = Shingle_len
        self.minhash_size = MinHash_size
        self.similarity_threshhold = Similarity_thresHOld
        with open(database) as f:
            content = f.readlines()
        self.DocList = [x.strip() for x in content]

        for file in self.DocList:
            self.DocObj.append(Shingling(file))
            print("Doc Name: ", file)
        print("Total Docs in Comparison: ", len(self.DocList))

    def getSimilarDocs(self):
        for i in range(len(self.DocObj)):
            for j in range(i + 1, len(self.DocObj)):
                similarity = self.DocObj[i].similarity(self.DocObj[j])
                if (similarity > self.similarity_threshhold):
                    print("Similarity level ABOVE THRESH HOLD for Doc: %s and Doc: %s is %.12f " % (
                        self.DocList[i], self.DocList[j], similarity))
                else:
                    print("Similarity level for Doc: %s and Doc: %s is %.12f " % (
                        self.DocList[i], self.DocList[j], similarity))


def starter():
    print("Entry point for the application: ")
    Starter_obj = CompareDocs("database.txt", 5, 100, 0.75)
    Starter_obj.getSimilarDocs()
    var = input()