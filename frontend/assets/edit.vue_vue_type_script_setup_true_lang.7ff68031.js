import{_ as x,D as h,C as S,v as R,t as U,F as q}from"./element-plus.f12e93f2.js";import{d as N,a as I,b as P,c as T}from"./department.1eb16518.js";import{P as M}from"./index.7735a16f.js";import{u as O}from"./useDictOptions.4c71d02c.js";import{f as L}from"./index.e3e224d5.js";import{d as X,s as E,r as $,e as j,a1 as z,o as F,c as G,X as o,P as r,u as l,O as H,T as J,a as _}from"./@vue.a137a740.js";const K={class:"edit-popup"},Q=_("div",{class:"form-tips"},"\u9ED8\u8BA4\u4E3A0\uFF0C \u6570\u503C\u8D8A\u5927\u8D8A\u6392\u524D",-1),ae=X({__name:"edit",emits:["success","close"],setup(W,{expose:D,emit:m}){const c=E(),n=E(),i=$("add"),B=j(()=>i.value=="edit"?"\u7F16\u8F91\u90E8\u95E8":"\u65B0\u589E\u90E8\u95E8"),u=z({id:"",pid:"",name:"",duty:"",mobile:"",sort:0,isStop:0}),b={pid:[{required:!0,message:"\u8BF7\u9009\u62E9\u4E0A\u7EA7\u90E8\u95E8",trigger:["change"]}],name:[{required:!0,message:"\u8BF7\u8F93\u5165\u90E8\u95E8\u540D\u79F0",trigger:["blur"]}],duty:[{required:!0,message:"\u8BF7\u8F93\u5165\u8D1F\u8D23\u4EBA\u59D3\u540D",trigger:["blur"]}],mobile:[{required:!0,message:"\u8BF7\u8F93\u5165\u8054\u7CFB\u7535\u8BDD",trigger:["blur"]},{validator:(t,e,d)=>{if(e){const s=/^[1][3,4,5,6,7,8,9][0-9]{9}$/;if(console.log(s.test(e)),s.test(e))d();else return d(new Error("\u8BF7\u8F93\u5165\u6B63\u786E\u7684\u624B\u673A\u53F7"))}else return d()},trigger:["blur"]}]},{optionsData:g}=O({dept:{api:N}}),V=async()=>{var t,e;await((t=c.value)==null?void 0:t.validate()),i.value=="edit"?await I(u):await P(u),(e=n.value)==null||e.close(),L.msgSuccess("\u64CD\u4F5C\u6210\u529F"),m("success")},v=(t="add")=>{var e;i.value=t,(e=n.value)==null||e.open()},f=t=>{for(const e in u)t[e]!=null&&t[e]!=null?u[e]=t[e]:u[e]=t.is_stop},A=async t=>{const e=await T({id:t.id});f(e)},y=()=>{m("close")};return D({open:v,setFormData:f,getDetail:A}),(t,e)=>{const d=x,s=h,p=S,C=R,w=U,k=q;return F(),G("div",K,[o(M,{ref_key:"popupRef",ref:n,title:l(B),async:!0,width:"550px",onConfirm:V,onClose:y},{default:r(()=>[o(k,{ref_key:"formRef",ref:c,model:l(u),"label-width":"84px",rules:b},{default:r(()=>[l(u).pid!==0?(F(),H(s,{key:0,label:"\u4E0A\u7EA7\u90E8\u95E8",prop:"pid"},{default:r(()=>[o(d,{class:"flex-1",modelValue:l(u).pid,"onUpdate:modelValue":e[0]||(e[0]=a=>l(u).pid=a),data:l(g).dept,clearable:"","node-key":"id",props:{value:"id",label:"name"},"check-strictly":"","default-expand-all":!0,placeholder:"\u8BF7\u9009\u62E9\u4E0A\u7EA7\u90E8\u95E8"},null,8,["modelValue","data"])]),_:1})):J("",!0),o(s,{label:"\u90E8\u95E8\u540D\u79F0",prop:"name"},{default:r(()=>[o(p,{modelValue:l(u).name,"onUpdate:modelValue":e[1]||(e[1]=a=>l(u).name=a),placeholder:"\u8BF7\u8F93\u5165\u90E8\u95E8\u540D\u79F0",clearable:"",maxlength:100},null,8,["modelValue"])]),_:1}),o(s,{label:"\u8D1F\u8D23\u4EBA",prop:"duty"},{default:r(()=>[o(p,{modelValue:l(u).duty,"onUpdate:modelValue":e[2]||(e[2]=a=>l(u).duty=a),placeholder:"\u8BF7\u8F93\u5165\u8D1F\u8D23\u4EBA\u59D3\u540D",clearable:"",maxlength:30},null,8,["modelValue"])]),_:1}),o(s,{label:"\u8054\u7CFB\u7535\u8BDD",prop:"mobile"},{default:r(()=>[o(p,{modelValue:l(u).mobile,"onUpdate:modelValue":e[3]||(e[3]=a=>l(u).mobile=a),placeholder:"\u8BF7\u8F93\u5165\u8054\u7CFB\u7535\u8BDD",clearable:""},null,8,["modelValue"])]),_:1}),o(s,{label:"\u6392\u5E8F",prop:"sort"},{default:r(()=>[_("div",null,[o(C,{modelValue:l(u).sort,"onUpdate:modelValue":e[4]||(e[4]=a=>l(u).sort=a),min:0,max:9999},null,8,["modelValue"]),Q])]),_:1}),o(s,{label:"\u90E8\u95E8\u72B6\u6001",prop:"isStop"},{default:r(()=>[o(w,{modelValue:l(u).isStop,"onUpdate:modelValue":e[5]||(e[5]=a=>l(u).isStop=a),"active-value":0,"inactive-value":1},null,8,["modelValue"])]),_:1})]),_:1},8,["model"])]),_:1},8,["title"])])}}});export{ae as _};
