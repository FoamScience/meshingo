import{b as r,o as a,w as s,g as e,z as n,v as u,x as m,C as t}from"./modules/vue-C-6iJnrv.js";import{_ as d}from"./slidev/two-cols.vue_vue_type_script_setup_true_lang-BIG59n98.js";import{u as p,f as g}from"./slidev/context-CSCw-8OC.js";import"./index-UP3SUwBt.js";import"./modules/shiki-Dsr63FLO.js";const v={__name:"03-critic.md__slidev_22",setup(f){const{$clicksContext:i,$frontmatter:o}=p();return i.setup(),(c,l)=>(a(),r(d,u(m(t(g)(t(o),21))),{right:s(N=>l[0]||(l[0]=[e("p",null,[e("br"),e("br")],-1),e("ul",null,[e("li",null,"Graph Neural Networks (GNNs) as replacement for Stage 1 as GNNs are better suited for learning spatial relationships in geometric data"),e("li",null,"Running a simple potential flow through the mesh can reveal where refinement is needed…"),e("li",null,"Doesn’t model discontinuities well, assuming smooth meshing responses…"),e("li",null,"Multi-scale geometries may require more than a single max-to-min cell size ratio"),e("li",null,[n("Heavily biases towards the "),e("code",null,"cartesianMesh"),n(" configuration (eg. no boundary layers… etc)")])],-1)])),default:s(()=>[l[1]||(l[1]=e("h1",null,"Critique and Discussions",-1)),l[2]||(l[2]=e("ul",null,[e("li",null,[n("Focusing on "),e("strong",null,"Automation & Unattended Meshing")]),e("li",null,"Data-Efficient Surrogate Model Training, not needing 1000s of STLs as a GNN/CNN would"),e("li",null,"BO is a good match since meshing operations can be so expensive")],-1)),l[3]||(l[3]=e("br",null,null,-1)),l[4]||(l[4]=e("ul",null,[e("li",null,[n("Mediocre handling of geometric features importances "),e("ul",null,[e("li",null,[e("code",null,"min(flatness*Cf, sharpness*Cs, ...)")]),e("li",null,"Maybe a CNN on voxalized STLs is better?")])])],-1))]),_:1},16))}};export{v as default};
