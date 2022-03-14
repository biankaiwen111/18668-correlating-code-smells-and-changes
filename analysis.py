import scipy.stats as stats

unchanged_classes_smells = []
changed_classes_smells = []

with open('./result.txt', 'r') as res:
    for line in res:
        commit = line.split(" ")
        if commit[0] == "None":
            continue
        unchanged_classes_smells.append(int(commit[0]))
        changed_classes_smells.append(int(commit[1]))

print(unchanged_classes_smells, len(unchanged_classes_smells))
print(changed_classes_smells, len(changed_classes_smells))

r = stats.mannwhitneyu(changed_classes_smells, unchanged_classes_smells, alternative='two-sided')
r1 = stats.mannwhitneyu(unchanged_classes_smells, changed_classes_smells, alternative='two-sided')
print(r)
print(r1)