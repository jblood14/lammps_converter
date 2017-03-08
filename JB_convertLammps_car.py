#####################################################################
#                                                                   #
#        Created by James W. Blood at Imperial College London       #
#                     j.blood14@imperial.ac.uk                      #
#     Distributed under the GNU General Public License Version 3    #
#                                                                   #
#####################################################################


lammps='final.lmps'
convert='types_forconvert.txt'

def ff_types(types_file):
    #Get ff atom types from types_forconvert.txt
    atom_types=[]
    with open(types_file) as atoms:
        for line in atoms:
            if 'atom' in line:
                continue
            elif 'bond' in line:
                break
            elif '#' in line:
                break
            else: 
                new_line=line.split()
                x=new_line[1]+((3-len(new_line[1]))*' ')
            atom_types.append((new_line[0],x,new_line[2]))
    return atom_types
f_type=ff_types(convert)
#run through lammps output to get box dimensions, charges and xyz
with open(lammps) as lmps:
    type_no=[]
    charges=[]
    atom_x=[]
    atom_y=[]
    atom_z=[]
    for line in lmps:
        #Box dimensions first
        if 'xlo' in line:
            new_line=line.split()
            x = float(new_line[1]) - float(new_line[0])
            print(x)
        elif 'ylo' in line:
            new_line=line.split()
            y = float(new_line[1]) - float(new_line[0])
        elif 'zlo' in line:
            new_line=line.split()
            z = float(new_line[1]) - float(new_line[0])
        if line.startswith('Atoms'):
            break
    for line in lmps:
        if 'Bonds' in line:
            break
        if line.startswith('\n'):
            continue
        new_line=line.split()
        type_no.append(new_line[2])
        charges.append(new_line[3])
        atom_x.append(new_line[4])
        atom_y.append(new_line[5])
        atom_z.append(new_line[6])
#Clean the data so all the same length
clean_x=[]
clean_y=[]
clean_z=[]
clean_c=[]
for a in atom_x:
    a=str(a)
    if len(a)==8:
        a=' '+a
    clean_x.append(a)
for b in atom_y:
    b=str(b)
    if len(b)==8:
        b=' '+b
    clean_y.append(b)
for c in atom_z:
    c=str(c)
    if len(c)==8:
        c=' '+c
    clean_z.append(c)
for c in charges:
    if len(c)==8:
        c=' '+c
    clean_c.append(c)

        
#write .car file
car=open('new_gulp.car','w')
#write the gubbins at the top
car.write('!BIOSYM archive 3\nPBC=ON\nTITLE!\nDATE!\n')
#Give PBC lengths and angles(always cubic)
car.write('PBC   '+str(x)[:7]+'   '+str(y)[:7]+'   '+str(z)[:7]+'   90.0000   90.0000   90.0000 (unknown)\n')
#write the atom details
atom_no=0
while atom_no<len(charges):
    for f in f_type:
        if type_no[atom_no] == f[0]: 
            car.write(f[2]+'       '+clean_x[atom_no]+'      '+clean_y[atom_no]+'      '+clean_z[atom_no]+
                      '    CORE '+str(atom_no+1)+(' '*(7-len(str(atom_no+1))))+f[1]+'     '
                      +f[2]+'  '+clean_c[atom_no][:6]+'\n')
    atom_no+=1
#end file
car.write('end\nend')
car.close()
