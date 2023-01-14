import csv
s='\u0020'
s4,s8,c_n,p_n,p_d=s*4,s*8,'',[],[]
for idx,row in enumerate(csv.reader(open('entity.csv','r'))):
 if idx==0:
  c_n=row[0]
  continue
 p_n.append(row[0])
 p_d.append(row[1])
i=''.join([f'{s8}self._{p_n[i]}{s}={s}\'{p_d[i]}\'\n' for i in range(len(p_n))])
g=''.join([f'{s4}@property\n{s4}def{s}{name}(self):\n{s8}return{s}self._{name}\n\n' for name in p_n])
t=''.join([f'{s4}@{name}.setter\n{s4}def{s}{name}(self,{s}{name}):\n{s8}self._{name}{s}={s}{name}\n\n' for name in p_n])
open(f'{str.lower(c_n)}.py','w',encoding='utf-8').write(f'class{s}{c_n}:\n{s4}def{s}__init__(self):\n{i}\n{g}\n{t}')