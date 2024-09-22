import slate3k


source_file = '/media/sf_dev/Dropbox/Jerry GA/AI SLR Project Journal Update V2/JM/2020 JM/Vol 84 Issue 1 Jan 2020/Berger et al JM 2020.pdf'
with open(source_file, 'rb') as file_in:
    doc = slate3k.PDF(file_in)

for page in doc:
    for line in page.split('\n'):
        if line.strip():
            print(line)
