[![Build Status](https://travis-ci.org/spaceship-labs/ctgen.svg)](https://travis-ci.org/spaceship-labs/ctgen)

# Scrapper de Compranet

## Ejecutar

```
node bin/ctgen.js install --no-mongo
```

Para subir a S3:

```
node bin/ctgen.js install --no-mongo --aws-id YYYYYYYYYYYY --aws-secret XXXXXXXXXXXXXXXXX --aws-region us-west-2 --aws-bucket bucket --aws-dir carpeta/del/bucket

```

## Procesos

1. Ejecuta `runAll` dentro de *main.js*
2. Busca y descarga los archivos ejecutando `getCsv` dentro de la carpeta **ctbook_files_xls**. Las fuentes y URL a las que accede son las siguientes:
    - Contrataciónes (*contrataciones*): https://sites.google.com/site/cnetuc/contrataciones
    - Contratos CompraNET3 (*cnet3*): https://sites.google.com/site/cnetuc/contratos_cnet_3 
    - Unidades Compradoras (*uc*): 
    http://upcp.funcionpublica.gob.mx/descargas/UC.zip
3. Transforma los archivos excel en CSV ejecutando `format.xls2csv` 

### Proceso con mongo

Cuando **CTGEN** se ejecuta sin la opción `--no-mongo`, al acabar las transformaciones, ejecuta `runMongo` que a su vez ejecuta `scripts.runScriptsMongo` con la lista de los archivos en CSV.

`scripts.runScriptsMongo` importa los CSV de *contrataciónes*, *cnet3* y *uc* en el mongo especificado (o local si no existen parámetros). Posteriormente ejecuta los siguientes scripts sobre los datos:

1. scripts/mongo/**04.index.js**: Crea índices sobre todas las tablas.
2. scripts/mongo/**05.empresas.js**: Extraé las empresas existentes a partir de la tabla de contratos haciendo los ajustes necesarios para Compranet3 
3. scripts/mongo/**05.01.fecha_inicio.js**: Actualiza las fechas para que cumplan formato estandar.
4. scripts/mongo/**06.00.dependencias.js**: Join de dependencias con unidades compradoras
5. scripts/mongo/**06.01.link.js**: Genera relación entre dependencia y unidad compradora a partir de tabla intermedia generada en el script anterior. Además inserta y asocia contratos a las dependencias no encontradas e inserta y actualiza contratos con unidades compradoras no encontradas.
6. scripts/mongo/**06.02.index.js**: Genera índices a las tablas que almacenarán a los proveedores de contratistas, los importes y las dependencias
7. scripts/mongo/**08.extract_duplicated**: Valida que no existan empresas duplicadas.

## Installation

```
# npm install ctgen -g
```

## Use

```
$ ctgen install -d namedb
```
```
$ ctgen --help
```
## Use auth

```
$ ctgen install -d ctbook --verbose -u ctbook -p "password"
```


## Test

```
$ npm install
```
```
$ npm test
```
