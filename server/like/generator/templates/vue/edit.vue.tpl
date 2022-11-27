<template>
    <div class="edit-popup">
        <popup
            ref="popupRef"
            :title="popupTitle"
            :async="true"
            width="550px"
            :clickModalClose="true"
            @confirm="handleSubmit"
            @close="handleClose"
        >
            <el-form ref="formRef" :model="formData" label-width="84px" :rules="formRules">
            {%- for column in columns %}
            {%- if column.is_edit %}
            {%- if table.tree_parent!="" and column.java_field==table.tree_parent %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-tree-select
                        class="flex-1"
                        v-model="formData.{{{ column.java_field }}}"
                        :data="treeList"
                        clearable
                        node-key="{{{ table.tree_primary }}}"
                        :props="{ label: '{{{ table.tree_name }}}', value: '{{{ table.tree_primary }}}', children: 'children' }"
                        :default-expand-all="true"
                        placeholder="请选择{{{ column.column_comment }}}"
                        check-strictly
                    />
                </el-form-item>
            {%- elif column.html_type=="input" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-input v-model="formData.{{{ column.java_field }}}" placeholder="请输入{{{ column.column_comment }}}" />
                </el-form-item>
            {%- elif column.html_type=="number" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-input-number v-model="formData.{{{ column.java_field }}}" :max="9999" />
                </el-form-item>
            {%- elif column.html_type=="textarea" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-input
                        v-model="formData.{{{ column.java_field }}}"
                        placeholder="请输入{{{ column.column_comment }}}"
                        type="textarea"
                        :autosize="{ minRows: 4, maxRows: 6 }"
                    />
                </el-form-item>
            {%- elif column.html_type=="checkbox" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-checkbox-group v-model="formData.{{{ column.java_field }}}" placeholder="请选择{{{ column.column_comment }}}">
                        {%- if column.dict_type!="" %}
                        <el-checkbox
                            v-for="(item, index) in dictData.{{{ column.dict_type }}}"
                            :key="index"
                            :label="item.value"
                            :disabled="!item.status"
                        >
                            {{ item.name }}
                        </el-checkbox>
                        {%- else %}
                        <el-checkbox>请选择字典生成</el-checkbox>
                        {%- endif %}
                    </el-checkbox-group>
                </el-form-item>
            {%- elif column.html_type=="select" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-select class="flex-1" v-model="formData.{{{ column.java_field }}}" placeholder="请选择{{{ column.column_comment }}}">
                        {%- if column.dict_type!="" %}
                        <el-option
                            v-for="(item, index) in dictData.{{{ column.dict_type }}}"
                            :key="index"
                            :label="item.name"
                            {%- if column.java_type == "Integer" %}
                            :value="parseInt(item.value)"
                            {%- else %}
                            :value="item.value"
                            {%- endif %}
                            clearable
                            :disabled="!item.status"
                        />
                        {%- else %}
                        <el-option label="请选择字典生成" value="" />
                        {%- endif %}
                    </el-select>
                </el-form-item>
            {%- elif column.html_type=="radio" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-radio-group v-model="formData.{{{ column.java_field }}}" placeholder="请选择{{{ column.column_comment }}}">
                        {%- if column.dict_type!="" %}
                        <el-radio
                            v-for="(item, index) in dictData.{{{ column.dict_type }}}"
                            :key="index"
                            {%- if column.java_type == "Integer" %}
                            :label="parseInt(item.value)"
                            {%- else %}
                            :label="item.value"
                            {%- endif %}
                            :disabled="!item.status"
                        >
                            {{ item.name }}
                        </el-radio>
                        {%- else %}
                        <el-radio label="0">请选择字典生成</el-radio>
                        {%- endif %}
                    </el-radio-group>
                </el-form-item>
            {%- elif column.html_type=="datetime" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <el-date-picker
                        class="flex-1 !flex"
                        v-model="formData.{{{ column.java_field }}}"
                        type="datetime"
                        clearable
                        value-format="YYYY-MM-DD hh:mm:ss"
                        placeholder="请选择{{{ column.column_comment }}}"
                    />
                </el-form-item>
            {%- elif column.html_type=="editor" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <editor v-model="formData.{{{ column.java_field }}}" :height="500" />
                </el-form-item>
            {%- elif column.html_type=="imageUpload" %}
                <el-form-item label="{{{ column.column_comment }}}" prop="{{{ column.java_field }}}">
                    <material-picker v-model="formData.{{{ column.java_field }}}" />
                </el-form-item>
            {%- endif %}
            {%- endif %}
            {%- endfor %}
            </el-form>
        </popup>
    </div>
</template>
<script lang="ts" setup>
import type { FormInstance } from 'element-plus'
import { {% if table.tree_primary and table.tree_parent %}{{{ module_name }}}Lists,{% endif %} {{{ module_name }}}Edit, {{{ module_name }}}Add, {{{ module_name }}}Detail } from '@/api/{{{ module_name }}}'
import Popup from '@/components/popup/index.vue'
import feedback from '@/utils/feedback'
import type { PropType } from 'vue'
defineProps({
    dictData: {
        type: Object as PropType<Record<string, any[]>>,
        default: () => ({})
    }
})
const emit = defineEmits(['success', 'close'])
const formRef = shallowRef<FormInstance>()
const popupRef = shallowRef<InstanceType<typeof Popup>>()
{%- if table.tree_primary and table.tree_parent %}
const treeList = ref<any[]>([])
{%- endif %}
const mode = ref('add')
const popupTitle = computed(() => {
    return mode.value == 'edit' ? '编辑{{{ function_name }}}' : '新增{{{ function_name }}}'
})

const formData = reactive({
    {%- for column in columns %}
    {%- if column.java_field==primary_key %}
    {{{ primary_key }}}: '',
    {%- elif column.is_edit %}
    {%- if column.html_type=="checkbox" %}
    {{{ column.java_field }}}: [],
    {%- elif column.html_type=="number" %}
    {{{ column.java_field }}}: 0,
    {%- else %}
    {{{ column.java_field }}}: '',
    {%- endif %}
    {%- endif %}
    {%- endfor %}
})

const formRules = {
    {%- for column in columns %}
    {%- if column.is_edit and column.is_required %}
    {{{ column.java_field }}}: [
        {
            required: true,
            {%- if column.html_type=="checkbox" or column.html_type=="datetime" or column.html_type=="radio" or column.html_type=="select" or column.html_type=="imageUpload" %}
            message: '请选择{{{ column.column_comment }}}',
            {%- else %}
            message: '请输入{{{ column.column_comment }}}',
            {%- endif %}
            trigger: ['blur']
        }
    ],
    {%- endif %}
    {%- endfor %}
}

const handleSubmit = async () => {
    await formRef.value?.validate()
    const data: any = { ...formData }
    {%- for column in columns %}
    {%- if column.html_type == "checkbox" %}
    data.{{{ column.java_field }}} = data.{{{ column.java_field }}}.join(',')
    {%- endif %}
    {%- endfor %}
    mode.value == 'edit' ? await {{{ module_name }}}Edit(data) : await {{{ module_name }}}Add(data)
    popupRef.value?.close()
    feedback.msgSuccess('操作成功')
    emit('success')
}

const open = (type = 'add') => {
    mode.value = type
    popupRef.value?.open()
}

const setFormData = async (data: Record<string, any>) => {
    for (const key in formData) {
        if (data[key] != null && data[key] != undefined) {
            //@ts-ignore
            formData[key] = data[key]
            {%- for column in columns %}
            {%- if column.html_type == "checkbox" %}
            //@ts-ignore
            formData.{{{ column.java_field }}} = String(data.{{{ column.java_field }}}).split(',')
            {%- endif %}
            {%- endfor %}
        }
    }
}

const getDetail = async (row: Record<string, any>) => {
    const data = await {{{ module_name }}}Detail({
        {{{ primary_key }}}: row.{{{ primary_key }}}
    })
    setFormData(data)
}

const handleClose = () => {
    emit('close')
}
{%- if table.tree_primary and table.tree_parent %}

const getLists = async () => {
    const data: any = await {{{ module_name }}}Lists()
    const item = { {{{ table.tree_primary }}}: 0, {{{ table.tree_name }}}: '顶级', children: [] }
    item.children = data
    treeList.value.push(item)
}

getLists()
{%- endif %}

defineExpose({
    open,
    setFormData,
    getDetail
})
</script>
