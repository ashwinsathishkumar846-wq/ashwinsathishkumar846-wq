# Mini notebook executor: runs code cells in one namespace, captures stdout / DataFrames / figures per cell
import sys, io, os, ast, json, time, traceback, contextlib
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL','2'); os.environ.setdefault('MPLBACKEND','Agg')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':14,'axes.titlesize':15,'axes.labelsize':14,'xtick.labelsize':12.5,'ytick.labelsize':12.5,'legend.fontsize':12.5,'figure.titlesize':16,'axes.titleweight':'bold'})
def run_notebook(name, cells, outdir, workdir):
    os.makedirs(outdir, exist_ok=True); os.chdir(workdir)
    ns={'__name__':'__main__'}; res=[]; figno=0
    def display(o):
        h=o._repr_html_() if hasattr(o,'_repr_html_') else None
        cur['html'].append(h) if h else print(repr(o))
    ns['display']=display
    for ci,(title,code) in enumerate(cells):
        cur={'title':title,'code':code,'text':'','html':[],'figs':[]}
        buf=io.StringIO(); t0=time.time()
        run_code='\n'.join(l for l in code.split('\n') if not l.startswith('!'))
        try:
            tree=ast.parse(run_code)
            last=None
            if tree.body and isinstance(tree.body[-1],ast.Expr) and not (isinstance(tree.body[-1].value,ast.Call) and getattr(tree.body[-1].value.func,'attr','') in ('show','summary','subplots_adjust','tight_layout')):
                last=ast.Expression(tree.body.pop().value)
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
                exec(compile(tree,'<cell>','exec'),ns)
                if last is not None:
                    v=eval(compile(last,'<cell>','eval'),ns)
                    if v is not None: display(v)
        except Exception:
            buf.write(traceback.format_exc()); print('ERROR in cell',ci,title,file=sys.__stdout__); print(traceback.format_exc(),file=sys.__stdout__)
        cur['text']=buf.getvalue()
        for n in plt.get_fignums():
            fig=plt.figure(n); fn=f'{outdir}/{name}_fig{figno:02d}.png'; fig.savefig(fn,dpi=200,bbox_inches='tight',facecolor='white'); cur['figs'].append(fn); figno+=1
        plt.close('all')
        cur['secs']=round(time.time()-t0,1); res.append(cur)
        print(f'[{name}] cell {ci} "{title}" done in {cur["secs"]}s',file=sys.__stdout__,flush=True)
        json.dump(res,open(f'{outdir}/{name}.json','w'))
    return res
