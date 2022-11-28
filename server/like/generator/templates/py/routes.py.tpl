import logging

from fastapi import APIRouter, Depends

from {{{ package_name }}}.schema_base import PageInationResult
from {{{ package_name }}}.http_base import unified_resp
from .schemas import (
    {{{ entity_name }}}ListIn, {{{ entity_name }}}DetailIn, {{{ entity_name }}}AddIn, 
    {{{ entity_name }}}EditIn, {{{ entity_name }}}DelIn, {{{ entity_name }}}Out)
from .service import I{{{ entity_name }}}Service, {{{ entity_name }}}Service

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api')


@router.get('/{{{ module_name }}}/list'{% if table.gen_tpl == 'crud' %}, response_model=PageInationResult[{{{ entity_name }}}Out]{% endif %})
@unified_resp
async def {{{ module_name }}}_list(
        list_in: {{{ entity_name }}}ListIn = Depends(),
        {{{ entity_snake_name }}}_service: I{{{ entity_name }}}Service = Depends({{{ entity_name }}}Service.instance)):
    """{{{ function_name }}}列表"""
    return await {{{ entity_snake_name }}}_service.list(list_in)


@router.get('/{{{ module_name }}}/detail')
@unified_resp
async def {{{ module_name }}}_detail(
        detail_in: {{{ entity_name }}}DetailIn = Depends(),
        {{{ entity_snake_name }}}_service: I{{{ entity_name }}}Service = Depends({{{ entity_name }}}Service.instance)):
    """{{{ function_name }}}详情"""
    return await {{{ entity_snake_name }}}_service.detail(detail_in.id)


@router.post('/{{{ module_name }}}/add')
@unified_resp
async def {{{ module_name }}}_add(
        add_in: {{{ entity_name }}}AddIn,
        {{{ entity_snake_name }}}_service: I{{{ entity_name }}}Service = Depends({{{ entity_name }}}Service.instance)):
    """{{{ function_name }}}新增"""
    return await {{{ entity_snake_name }}}_service.add(add_in)


@router.post('/{{{ module_name }}}/edit')
@unified_resp
async def {{{ module_name }}}_edit(
        edit_in: {{{ entity_name }}}EditIn,
        {{{ entity_snake_name }}}_service: I{{{ entity_name }}}Service = Depends({{{ entity_name }}}Service.instance)):
    """{{{ function_name }}}编辑"""
    return await {{{ entity_snake_name }}}_service.edit(edit_in)


@router.post('/{{{ module_name }}}/del')
@unified_resp
async def {{{ module_name }}}_del(
        del_in: {{{ entity_name }}}DelIn,
        {{{ entity_snake_name }}}_service: I{{{ entity_name }}}Service = Depends({{{ entity_name }}}Service.instance)):
    """{{{ function_name }}}删除"""
    return await {{{ entity_snake_name }}}_service.delete(del_in.id)
