import{d as F,r as C,O as N,A as i,P as $,f as c,g as e,k as g,C as l,e as a,w as r,t as z,F as T,o as u}from"../modules/vue-BUK1fca5.js";import{k as B,l as D,s as d,n as E,o as H,p as L}from"../index-CmGySMzI.js";import{_ as V,C as A}from"./NoteDisplay.vue_vue_type_style_index_0_lang-CbEk0dLz.js";import{_ as f}from"./IconButton.vue_vue_type_script_setup_true_lang-DMUwaWBW.js";import"../modules/shiki-Juy2Ldrq.js";const I={class:"h-full pt-2 flex flex-col"},M={class:"flex-none border-t border-main",px3:"",py2:""},O={class:"flex-none border-t border-main"},P={class:"flex gap-1 items-center px-6 py-3"},R={key:0,class:"i-carbon:minimize"},j={key:1,class:"i-carbon:maximize"},q={class:"p2 text-center"},X=F({__name:"notes",setup(G){B({title:`Notes - ${L}`});const{slides:b,total:m}=D(),{isFullscreen:p,toggle:y}=H,v=C(),s=N("slidev-notes-font-size",18),n=i(()=>d.page),_=i(()=>b.value.find(o=>o.no===n.value));$(n,()=>{var o;(o=v.value)==null||o.scrollTo({left:0,top:0,behavior:"smooth"}),window.scrollTo({left:0,top:0,behavior:"smooth"})});function S(){s.value=s.value+1}function w(){s.value=s.value-1}const x=i(()=>{const o=d.clicks,t=d.clicksTotal;return E(C(o),void 0,t)});return(o,t)=>{var k,h;return u(),c(T,null,[e("div",{class:"fixed top-0 left-0 h-3px bg-primary transition-all duration-500",style:g({width:`${(n.value-1)/(l(m)-1)*100+1}%`})},null,4),e("div",I,[e("div",{ref_key:"scroller",ref:v,class:"px-5 flex-auto h-full overflow-auto",style:g({fontSize:`${l(s)}px`})},[a(V,{note:(k=_.value)==null?void 0:k.meta.slide.note,"note-html":(h=_.value)==null?void 0:h.meta.slide.noteHTML,placeholder:`No notes for Slide ${n.value}.`,"clicks-context":x.value,"auto-scroll":!0},null,8,["note","note-html","placeholder","clicks-context"])],4),e("div",M,[a(A,{"clicks-context":x.value,readonly:""},null,8,["clicks-context"])]),e("div",O,[e("div",P,[a(f,{title:l(p)?"Close fullscreen":"Enter fullscreen",onClick:l(y)},{default:r(()=>[l(p)?(u(),c("div",R)):(u(),c("div",j))]),_:1},8,["title","onClick"]),a(f,{title:"Increase font size",onClick:S},{default:r(()=>t[0]||(t[0]=[e("div",{class:"i-carbon:zoom-in"},null,-1)])),_:1}),a(f,{title:"Decrease font size",onClick:w},{default:r(()=>t[1]||(t[1]=[e("div",{class:"i-carbon:zoom-out"},null,-1)])),_:1}),t[2]||(t[2]=e("div",{class:"flex-auto"},null,-1)),e("div",q,z(n.value)+" / "+z(l(m)),1)])])])],64)}}});export{X as default};
