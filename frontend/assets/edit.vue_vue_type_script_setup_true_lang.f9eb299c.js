import{O as w,P as g,C as k,D as v,F as E}from"./element-plus.ecace360.js";import{P as x}from"./index.ac78db26.js";import{f as T,g as D}from"./dict.e301c9b5.js";import{f as N}from"./index.34b1f292.js";import{d as S,s as f,r as U,e as h,a1 as P,o as q,c as I,X as t,P as l,u as o,U as _}from"./@vue.a137a740.js";const z={class:"edit-popup"},L=S({__name:"edit",emits:["success","close"],setup(A,{expose:B,emit:n}){const p=f(),r=f(),i=U("add"),F=h(()=>i.value=="edit"?"\u7F16\u8F91\u5B57\u5178\u7C7B\u578B":"\u65B0\u589E\u5B57\u5178\u7C7B\u578B"),u=P({id:"",dictName:"",dictType:"",dictStatus:1,dictRemark:""}),C={dictName:[{required:!0,message:"\u8BF7\u8F93\u5165\u5B57\u5178\u540D\u79F0",trigger:["blur"]}],dictType:[{required:!0,message:"\u8BF7\u8F93\u5165\u5B57\u5178\u7C7B\u578B",trigger:["blur"]}]},b=async()=>{var a,e;await((a=p.value)==null?void 0:a.validate()),i.value=="edit"?await T(u):await D(u),(e=r.value)==null||e.close(),N.msgSuccess("\u64CD\u4F5C\u6210\u529F"),n("success")},V=()=>{n("close")};return B({open:(a="add")=>{var e;i.value=a,(e=r.value)==null||e.open()},setFormData:a=>{for(const e in u)a[e]!=null&&a[e]!=null&&(u[e]=a[e])}}),(a,e)=>{const m=k,s=v,c=w,y=g,R=E;return q(),I("div",z,[t(x,{ref_key:"popupRef",ref:r,title:o(F),async:!0,width:"550px",onConfirm:b,onClose:V},{default:l(()=>[t(R,{class:"ls-form",ref_key:"formRef",ref:p,rules:C,model:o(u),"label-width":"84px"},{default:l(()=>[t(s,{label:"\u5B57\u5178\u540D\u79F0",prop:"dictName"},{default:l(()=>[t(m,{modelValue:o(u).dictName,"onUpdate:modelValue":e[0]||(e[0]=d=>o(u).dictName=d),placeholder:"\u8BF7\u8F93\u5165\u5B57\u5178\u540D\u79F0",clearable:""},null,8,["modelValue"])]),_:1}),t(s,{label:"\u5B57\u5178\u7C7B\u578B",prop:"dictType"},{default:l(()=>[t(m,{modelValue:o(u).dictType,"onUpdate:modelValue":e[1]||(e[1]=d=>o(u).dictType=d),placeholder:"\u8BF7\u8F93\u5165\u5B57\u5178\u7C7B\u578B",clearable:""},null,8,["modelValue"])]),_:1}),t(s,{label:"\u5B57\u5178\u72B6\u6001",required:"",prop:"dictStatus"},{default:l(()=>[t(y,{modelValue:o(u).dictStatus,"onUpdate:modelValue":e[2]||(e[2]=d=>o(u).dictStatus=d)},{default:l(()=>[t(c,{label:1},{default:l(()=>[_("\u6B63\u5E38")]),_:1}),t(c,{label:0},{default:l(()=>[_("\u505C\u7528")]),_:1})]),_:1},8,["modelValue"])]),_:1}),t(s,{label:"\u5907\u6CE8",prop:"dictRemark"},{default:l(()=>[t(m,{modelValue:o(u).dictRemark,"onUpdate:modelValue":e[3]||(e[3]=d=>o(u).dictRemark=d),type:"textarea",autosize:{minRows:4,maxRows:6},clearable:"",maxlength:"200","show-word-limit":""},null,8,["modelValue"])]),_:1})]),_:1},8,["model"])]),_:1},8,["title"])])}}});export{L as _};
