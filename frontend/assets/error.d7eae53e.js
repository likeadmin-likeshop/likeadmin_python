import{w as l}from"./element-plus.f12e93f2.js";import{a as u}from"./vue-router.9605b890.js";import{d,r as _,H as v,o as n,c as f,a as r,K as B,V as i,O as x,P as y,U as g,u as E,T as h}from"./@vue.a137a740.js";import{d as k}from"./index.e3e224d5.js";import"./@vueuse.07613b64.js";import"./@element-plus.3660753f.js";import"./lodash-es.a31ceab4.js";import"./dayjs.b0476e70.js";import"./axios.9640b842.js";import"./async-validator.fb49d0f5.js";import"./@ctrl.82a509e0.js";import"./@popperjs.36402333.js";import"./escape-html.e5dfadb9.js";import"./normalize-wheel-es.8aeb3683.js";import"./lodash.3fb3ef02.js";import"./pinia.9b4180ce.js";import"./css-color-function.a13f8320.js";import"./color.7afdf413.js";import"./clone.8bef1d37.js";import"./color-convert.755d189f.js";import"./color-name.e7a4e1d3.js";import"./color-string.e356f5de.js";import"./balanced-match.d2a36341.js";import"./ms.564e106c.js";import"./nprogress.d3ae6d3f.js";import"./vue-clipboard3.0f0c7a0b.js";import"./clipboard.863e7101.js";import"./echarts.7e912674.js";import"./zrender.754e8e90.js";import"./tslib.60310f1a.js";import"./highlight.js.7165574c.js";import"./@highlightjs.7fc78ec7.js";const w={class:"error"},C={class:"error-code"},D={class:"text-lg text-tx-secondary mt-7 mb-7"},I=d({__name:"error",props:{code:String,title:String,showBtn:{type:Boolean,default:!0}},setup(t){const m=t;let o=null;const e=_(5),s=u();return m.showBtn&&(o=setInterval(()=>{e.value===0?(clearInterval(o),s.go(-1)):e.value--},1e3)),v(()=>{o&&clearInterval(o)}),(p,a)=>{const c=l;return n(),f("div",w,[r("div",null,[B(p.$slots,"content",{},()=>[r("div",C,i(t.code),1)],!0),r("div",D,i(t.title),1),t.showBtn?(n(),x(c,{key:0,type:"primary",onClick:a[0]||(a[0]=S=>E(s).go(-1))},{default:y(()=>[g(i(e.value)+" \u79D2\u540E\u8FD4\u56DE\u4E0A\u4E00\u9875 ",1)]),_:1})):h("",!0)])])}}});const nt=k(I,[["__scopeId","data-v-a47523cc"]]);export{nt as default};
