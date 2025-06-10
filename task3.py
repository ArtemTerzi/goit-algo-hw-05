import timeit

def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    if len(pattern) == 0:
        return 0
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    if M == 0:
        return 0
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1, modulus)
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    if substring_length == 0:
        return 0
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1, modulus)
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            if current_slice_hash < 0:
                current_slice_hash += modulus
    return -1

def load_text(filename, format):
    with open(filename, encoding=format) as f:
        return f.read()

article1 = load_text('./files/article1.txt', 'cp1251')
article2 = load_text('./files/article2.txt', 'utf-8')

pattern_real_1 = "GPGPU"
pattern_fake_1 = "винахідник"

pattern_real_2 = "хеш-таблиці"
pattern_fake_2 = "прикольно"

def time_search(func, text, pattern, number=100):
    timer = timeit.Timer(lambda: func(text, pattern))
    time_taken = timer.timeit(number=number)
    return time_taken / number

results = {}

for article_name, article_text, real_p, fake_p in [
    ('Article 1', article1, pattern_real_1, pattern_fake_1),
    ('Article 2', article2, pattern_real_2, pattern_fake_2)
]:
    results[article_name] = {}
    for pattern_type, pattern in [('Real', real_p), ('Fake', fake_p)]:
        results[article_name][pattern_type] = {}
        bm_time = time_search(boyer_moore_search, article_text, pattern)
        kmp_time = time_search(kmp_search, article_text, pattern)
        rk_time = time_search(rabin_karp_search, article_text, pattern)
        results[article_name][pattern_type]['Boyer-Moore'] = bm_time
        results[article_name][pattern_type]['KMP'] = kmp_time
        results[article_name][pattern_type]['Rabin-Karp'] = rk_time

for article_name in results:
    print(f"\nРезультати для {article_name}:")
    for pattern_type in results[article_name]:
        print(f"  Підрядок: {pattern_type}")
        times = results[article_name][pattern_type]
        for alg in times:
            print(f"    {alg}: {times[alg]:.6f} с")
        # Найшвидший алгоритм
        fastest_alg = min(times, key=times.get)
        print(f"    -> Найшвидший алгоритм: {fastest_alg}")

print("\nЗагальне порівняння (усі тести):")
aggregate_times = {'Boyer-Moore': 0, 'KMP': 0, 'Rabin-Karp': 0}
count = 0
for article_name in results:
    for pattern_type in results[article_name]:
        count += 1
        for alg in aggregate_times:
            aggregate_times[alg] += results[article_name][pattern_type][alg]

for alg in aggregate_times:
    print(f"{alg}: {aggregate_times[alg] / count:.6f} с")

fastest_overall = min(aggregate_times, key=aggregate_times.get)
print(f"-> Найшвидший алгоритм загалом: {fastest_overall}")
