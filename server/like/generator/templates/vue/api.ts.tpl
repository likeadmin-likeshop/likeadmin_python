import request from '@/utils/request'

// {{{function_name}}}列表
export function {{{module_name}}}Lists(params?: Record<string, any>) {
    return request.get({ url: '/{{{module_name}}}/list', params })
}

// {{{function_name}}}详情
export function {{{module_name}}}Detail(params: Record<string, any>) {
    return request.get({ url: '/{{{module_name}}}/detail', params })
}

// {{{function_name}}}新增
export function {{{module_name}}}Add(params: Record<string, any>) {
    return request.post({ url: '/{{{module_name}}}/add', params })
}

// {{{function_name}}}编辑
export function {{{module_name}}}Edit(params: Record<string, any>) {
    return request.post({ url: '/{{{module_name}}}/edit', params })
}

// {{{function_name}}}删除
export function {{{module_name}}}Delete(params: Record<string, any>) {
    return request.post({ url: '/{{{module_name}}}/del', params })
}
