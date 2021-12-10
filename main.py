import pefile

#open PE file

pe = pefile.PE("calc.exe")

for section in pe.sections:
    print(f"Section Name: {section.Name}")

    section_hash = section.get_hash_md5()
    print(section_hash)

print("TimeDateStamp: "+ (pe.FILE_HEADER.TimeDateStamp))
