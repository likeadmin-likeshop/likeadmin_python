import{X as S,Q as N,R as L,C as M,w as U}from"./element-plus.ecace360.js";import{d as $,r as p,w as O,o as a,c as b,X as m,P as s,a as i,$ as k,K as P,O as c,u as f,k as v,W as A,a8 as D,U as x}from"./@vue.a137a740.js";import{c as R}from"./@vueuse.07613b64.js";const X={class:"popover-input__input mr-[10px] flex-1"},F={class:"popover-input__btns flex-none"},I=["onClick"],W=$({__name:"index",props:{value:{type:String},type:{type:String,default:"text"},width:{type:[Number,String],default:"300px"},placeholder:String,disabled:{type:Boolean,default:!1},options:{type:Array,default:()=>[]},size:{type:String,default:"default"},limit:{type:Number,default:200},showLimit:{type:Boolean,default:!1},teleported:{type:Boolean,default:!0}},emits:["confirm"],setup(e,{emit:h}){const y=e,n=p(!1),u=p(!1),o=p(),g=()=>{r(),h("confirm",o.value)},z=()=>{y.disabled||(n.value=!0)},r=()=>{n.value=!1};return O(()=>y.value,d=>{o.value=d},{immediate:!0}),R(document.documentElement,"click",()=>{u.value||r()}),(d,t)=>{const V=N,B=L,C=M,w=U,E=S;return a(),b("div",{onMouseenter:t[4]||(t[4]=l=>u.value=!0),onMouseleave:t[5]||(t[5]=l=>u.value=!1)},[m(E,{placement:"top",visible:f(n),"onUpdate:visible":t[3]||(t[3]=l=>v(n)?n.value=l:null),width:e.width,trigger:"contextmenu",class:"popover-input",teleported:e.teleported,persistent:!1,"popper-class":"!p-0"},{reference:s(()=>[i("div",{class:"inline",onClick:k(z,["stop"])},[P(d.$slots,"default")],8,I)]),default:s(()=>[i("div",{class:"flex p-3",onClick:t[2]||(t[2]=k(()=>{},["stop"]))},[i("div",X,[e.type=="select"?(a(),c(B,{key:0,class:"flex-1",size:e.size,modelValue:f(o),"onUpdate:modelValue":t[0]||(t[0]=l=>v(o)?o.value=l:null),teleported:e.teleported},{default:s(()=>[(a(!0),b(A,null,D(e.options,l=>(a(),c(V,{key:l.value,label:l.label,value:l.value},null,8,["label","value"]))),128))]),_:1},8,["size","modelValue","teleported"])):(a(),c(C,{key:1,modelValue:f(o),"onUpdate:modelValue":t[1]||(t[1]=l=>v(o)?o.value=l:null),modelModifiers:{trim:!0},maxlength:e.limit,"show-word-limit":e.showLimit,type:e.type,size:e.size,clearable:"",placeholder:e.placeholder},null,8,["modelValue","maxlength","show-word-limit","type","size","placeholder"]))]),i("div",F,[m(w,{link:"",onClick:r},{default:s(()=>[x("\u53D6\u6D88")]),_:1}),m(w,{type:"primary",size:e.size,onClick:g},{default:s(()=>[x("\u786E\u5B9A")]),_:1},8,["size"])])])]),_:3},8,["visible","width","teleported"])],32)}}});export{W as _};
