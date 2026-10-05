import content7,subprocess,os,json,select,time
tr={}
for k in content7.KEYS:
    e=content7.E[k]; open(f'p7/{k}.js','w').write(e['code'][0][1]); outs=[]
    for ans,prompts in e['runs']:
        p=subprocess.Popen(['node',f'p7/{k}.js'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,bufsize=0)
        buf='';res='';i=0;t0=time.time()
        while True:
            r,_,_=select.select([p.stdout],[],[],0.3)
            if r:
                ch=os.read(p.stdout.fileno(),1).decode()
                if ch=='': break
                buf+=ch;res+=ch
                if i<len(prompts) and buf.endswith(prompts[i]):
                    p.stdin.write((ans[i]+'\n').encode());p.stdin.flush();res+=ans[i]+'\n';i+=1;buf=''
            elif p.poll() is not None: break
            if time.time()-t0>10: p.kill();break
        outs.append(f'D:\\WT_LAB\\Programs\\Exp7>node exp{k}.js\n'+res.rstrip('\n'))
    tr[k]=outs
json.dump(tr,open('tr7.json','w'),indent=1)
for k,v in tr.items():
    print(k);[print(x,'\n---') for x in v]
