#!/usr/bin/env python

# Created by Raul Peralta-Lozada (28/09/17)
import pandas as pd


def proveedores_por_contrato(df):
    """Por cada unidad compradora calcula los proveedores diferentes por contrato"""
    monto_por_contrato = df.groupby(
        ['DEPENDENCIA', 'CLAVEUC', 'PROVEEDOR_CONTRATISTA',
         'NUMERO_PROCEDIMIENTO', 'CODIGO_CONTRATO'],
        as_index=False
    ).IMPORTE_PESOS.sum()
    # ----------
    pocs_distintos = monto_por_contrato.groupby('CLAVEUC').PROVEEDOR_CONTRATISTA.nunique()
    pocs_distintos = pocs_distintos.reset_index()
    pocs_distintos = pocs_distintos.rename(
      columns={'PROVEEDOR_CONTRATISTA': 'proveedores_distintos'})
    contratos_total = monto_por_contrato.groupby(
        ['CLAVEUC', 'NUMERO_PROCEDIMIENTO']).CODIGO_CONTRATO.nunique()
    contratos_total = contratos_total.reset_index()
    contratos_total = contratos_total.rename(columns={'CODIGO_CONTRATO': 'conteo_contratos'})
    contratos_total = contratos_total.groupby('CLAVEUC', as_index=False).conteo_contratos.sum()
    # nunique_provs/num_contatros
    df_feature = pd.merge(pocs_distintos, contratos_total, on='CLAVEUC', how='inner')
    df_feature = df_feature.assign(
        proveedores_por_contrato=df_feature.proveedores_distintos.divide(df_feature.conteo_contratos)
    )
    return df_feature.loc[:, ['CLAVEUC', 'proveedores_por_contrato']]


def porcentaje_procedimientos_por_tipo(df):
    """Por cada unidad compradora calcula el porcentaje de procedimientos por tipo"""
    monto_por_contrato = df.groupby(
        ['DEPENDENCIA', 'CLAVEUC', 'PROVEEDOR_CONTRATISTA', 'NUMERO_PROCEDIMIENTO',
         'CODIGO_CONTRATO', 'TIPO_PROCEDIMIENTO'],
        as_index=False
    ).IMPORTE_PESOS.sum()
    conteo_tipos = monto_por_contrato.groupby(
        ['CLAVEUC', 'TIPO_PROCEDIMIENTO']
    ).NUMERO_PROCEDIMIENTO.nunique().reset_index()
    conteo_tipos = conteo_tipos.pivot(
        index='CLAVEUC', columns='TIPO_PROCEDIMIENTO',
        values='NUMERO_PROCEDIMIENTO'
    ).fillna(0)
    total_procedimientos = conteo_tipos.sum(axis=1)
    conteo_tipos = conteo_tipos * 100
    conteo_tipos = conteo_tipos.divide(total_procedimientos, axis='index')
    # TODO: cambiar el nombre de las columnas
    conteo_tipos = conteo_tipos.reset_index()
    conteo_tipos.columns.name = ''
    return conteo_tipos


def porcentaje_monto_tipo_procedimiento(df):
    monto_por_contrato = df.groupby(
        ['DEPENDENCIA', 'CLAVEUC', 'PROVEEDOR_CONTRATISTA',
         'NUMERO_PROCEDIMIENTO', 'CODIGO_CONTRATO', 'TIPO_PROCEDIMIENTO'],
        as_index=False
    ).IMPORTE_PESOS.sum()
    monto_tipos = monto_por_contrato.groupby(
        ['CLAVEUC', 'TIPO_PROCEDIMIENTO'], as_index=False
    ).IMPORTE_PESOS.sum()
    monto_tipos = monto_tipos.pivot(
        index='CLAVEUC', columns='TIPO_PROCEDIMIENTO',
        values='IMPORTE_PESOS'
    ).fillna(0)
    total_montos = monto_tipos.sum(axis=1)
    monto_tipos = monto_tipos * 100
    monto_tipos = monto_tipos.divide(total_montos, axis='index')
    # TODO: cambiar el nombre de las columnas
    monto_tipos = monto_tipos.reset_index()
    monto_tipos.columns.name = ''
    return monto_tipos


def importe_promedio_por_contrato(df):
    monto_por_contrato = df.groupby(
        ['DEPENDENCIA', 'CLAVEUC', 'PROVEEDOR_CONTRATISTA',
         'NUMERO_PROCEDIMIENTO', 'CODIGO_CONTRATO'],
        as_index=False
    ).IMPORTE_PESOS.sum()

    contratos_total = monto_por_contrato.groupby(
        ['CLAVEUC', 'NUMERO_PROCEDIMIENTO']).CODIGO_CONTRATO.nunique()
    contratos_total = contratos_total.reset_index()
    contratos_total = contratos_total.rename(columns={'CODIGO_CONTRATO': 'conteo_contratos'})
    contratos_total = contratos_total.groupby('CLAVEUC', as_index=False).conteo_contratos.sum()

    monto_uc_contratos = monto_por_contrato.groupby(
        ['CLAVEUC', 'NUMERO_PROCEDIMIENTO', 'CODIGO_CONTRATO'], as_index=False
    ).IMPORTE_PESOS.sum()
    monto_uc_contratos = monto_uc_contratos.groupby('CLAVEUC', as_index=False).IMPORTE_PESOS.sum()

    df_feature = pd.merge(monto_uc_contratos, contratos_total, on='CLAVEUC', how='inner')
    df_feature = df_feature.assign(
        monto_contrato_promedio=df_feature.IMPORTE_PESOS.divide(df_feature.conteo_contratos)
    )
    return df_feature.loc[:, ['CLAVEUC', 'monto_contrato_promedio']]


def porcentaje_procedimientos_presenciales(df):
    monto_por_contrato = df.groupby(
        ['DEPENDENCIA', 'CLAVEUC', 'PROVEEDOR_CONTRATISTA',
         'NUMERO_PROCEDIMIENTO', 'CODIGO_CONTRATO', 'FORMA_PROCEDIMIENTO'],
        as_index=False
    ).IMPORTE_PESOS.sum()
    conteo_formas = monto_por_contrato.groupby(
        ['CLAVEUC', 'FORMA_PROCEDIMIENTO']
    ).NUMERO_PROCEDIMIENTO.nunique().reset_index()
    conteo_formas = conteo_formas.pivot(
        index='CLAVEUC', columns='FORMA_PROCEDIMIENTO',
        values='NUMERO_PROCEDIMIENTO'
    ).fillna(0)
    total_procedimientos = conteo_formas.sum(axis=1)
    conteo_formas = conteo_formas * 100
    conteo_formas = conteo_formas.divide(total_procedimientos, axis='index')
    # TODO: cambiar el nombre de las columnas
    conteo_formas = conteo_formas.reset_index()
    conteo_formas.columns.name = ''
    return conteo_formas
