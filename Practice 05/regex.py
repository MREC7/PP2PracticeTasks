import re
a = "abbbbb"
b = "abb"
c = "a_b_c aaa bbb ccc"
d = "AaBbCc ABC"
e = "a023090d909090b"
f = "Some simple sentence, really simple."
g = "some_words"
h = "Example Sentence"
i = "PythonIsCool"
j = "camelCase"
print(re.match(r"a(b*)", a)) #1
print(re.match(r"a(b{2,3})", b)) #2
print(re.match(r"[a-z]+(_[a-z]+)+", c)) #3
print(re.match(r"([A-Z]+([a-z]+))+", d)) #4
print(re.match(r"^a.+b$", e)) #5
print(re.sub(r"[ ,.]", ":", f)) #6
print(re.sub(r"_([a-z])", lambda m: m.group(1).upper(), g)) #7
print(re.split(r"(?=[A-Z])", h)) #8
print(re.sub(r"([a-z])([A-Z])", r"\1 \2", i)) #9
print((re.sub(r"([a-z])([A-Z])", r"\1_\2", j)).lower()) #10