from fastapi import FastAPI, APIRouter, Query, HTTPException, Response
import fdb
import os
from dotenv import load_dotenv
from datetime import datetime
from fastapi.responses import JSONResponse
from io import StringIO
import csv

# Carregar variáveis do .env
load_dotenv()

app = FastAPI()
router = APIRouter()

def get_firebird_conn():
    return fdb.connect(
        host=os.getenv("FIREBIRD_HOST"),
        database=os.getenv("FIREBIRD_DATABASE"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD"),
        charset=os.getenv("FIREBIRD_CHARSET"),
    )

def parse_date(date_str, param_name):
    try:
        # Aceita tanto 'DD/MM/YYYY' quanto 'YYYY-MM-DD'
        if "/" in date_str:
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        else:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=422, detail=f"Parâmetro de data inválido: {param_name} deve ser DD/MM/AAAA")

CAMPOS_NUMERICOS = {"valor_nf", "valor", "valor_pago", "conta", "NR_TERRENO"}
CAMPOS_DATAS = {"emissao", "vencimento", "pagamento", "dt_cancelado"}

def tratar_valor(col, v):
    if v is None or (isinstance(v, str) and v.strip() == ""):
        if col in CAMPOS_NUMERICOS:
            return 0
        if col in CAMPOS_DATAS:
            return ""
        return ""
    return v

@router.get("/consulta")
def consulta_cobranca(
    response: Response,
    pagamento_ini: str = Query(None),
    pagamento_fim: str = Query(None),
    vencimento_ini: str = Query(None),
    vencimento_fim: str = Query(None),
    nome: str = Query(None),
    pagina: int = Query(1, ge=1),
    limite: int = Query(100, ge=1, le=1000)
):
    filtros = []
    params = []
    # Pagamento
    if pagamento_ini:
        dt_ini = parse_date(pagamento_ini, "pagamento_ini")
        filtros.append("RECEBER.pagamento >= ?")
        params.append(dt_ini)
    if pagamento_fim:
        dt_fim = parse_date(pagamento_fim, "pagamento_fim")
        filtros.append("RECEBER.pagamento <= ?")
        params.append(dt_fim)
    # Vencimento
    if vencimento_ini:
        vdt_ini = parse_date(vencimento_ini, "vencimento_ini")
        filtros.append("RECEBER.vencimento >= ?")
        params.append(vdt_ini)
    if vencimento_fim:
        vdt_fim = parse_date(vencimento_fim, "vencimento_fim")
        filtros.append("RECEBER.vencimento <= ?")
        params.append(vdt_fim)
    # Nome
    if nome:
        filtros.append("LOWER(TRIM(t.razao)) LIKE ?")
        params.append(f"%{nome.strip().lower()}%")
    
    offset = (pagina - 1) * limite

    sql = f"""
    SELECT FIRST {limite} SKIP {offset}
        RECEBER.numero, 
        t.razao AS Nome, 
        RECEBER.valor_nf, 
        RECEBER.emissao, 
        RECEBER.vencimento, 
        RECEBER.valor, 
        RECEBER.pagamento, 
        RECEBER.valor_pago, 
        RECEBER.referente_a, 
        t.cgc,
        t.telefone, 
        t.fax, 
        t.fone_comercial, 
        t.endereco, 
        t.bairro, 
        t.cidade, 
        t.uf, 
        t.cep, 
        t.email, 
        t.obs, 
        RECEBER.conta
    FROM RECEBER 
    JOIN TITULAR t ON t.Codigo = RECEBER.TITULAR 
    """
    if filtros:
        sql += "\nWHERE " + " AND ".join(filtros)

    sql_count = """
    SELECT COUNT(*)
    FROM RECEBER 
    JOIN TITULAR t ON t.Codigo = RECEBER.TITULAR 
    """
    if filtros:
        sql_count += "\nWHERE " + " AND ".join(filtros)

    try:
        conn = get_firebird_conn()
        cur = conn.cursor()
        try:
            print("DEBUG SQL:", sql)
            print("DEBUG PARAMS:", params)
            cur.execute(sql_count, params)
            total_registros = cur.fetchone()[0]
            cur.execute(sql, params)
            columns = [desc[0].lower() for desc in cur.description]
            rows = cur.fetchall()
        finally:
            try: cur.close()
            except: pass
            try: conn.close()
            except: pass

        result = []
        for row in rows:
            d = {}
            for col, val in zip(columns, row):
                d[col] = tratar_valor(col, val)
            result.append(d)

        return {
            "status": "ok",
            "pagina": pagina,
            "limite": limite,
            "total_registros": total_registros,
            "dados": result
        }
    except Exception as e:
        response.status_code = 500
        return {"status": "erro", "mensagem": f"Erro ao executar consulta: {str(e)}"}

@router.get("/consulta_csv")
def exporta_csv_cobranca(
    pagamento_ini: str = Query(None),
    pagamento_fim: str = Query(None),
    vencimento_ini: str = Query(None),
    vencimento_fim: str = Query(None),
    nome: str = Query(None)
):
    filtros = []
    params = []
    # Pagamento
    if pagamento_ini:
        dt_ini = parse_date(pagamento_ini, "pagamento_ini")
        filtros.append("RECEBER.pagamento >= ?")
        params.append(dt_ini)
    if pagamento_fim:
        dt_fim = parse_date(pagamento_fim, "pagamento_fim")
        filtros.append("RECEBER.pagamento <= ?")
        params.append(dt_fim)
    # Vencimento
    if vencimento_ini:
        vdt_ini = parse_date(vencimento_ini, "vencimento_ini")
        filtros.append("RECEBER.vencimento >= ?")
        params.append(vdt_ini)
    if vencimento_fim:
        vdt_fim = parse_date(vencimento_fim, "vencimento_fim")
        filtros.append("RECEBER.vencimento <= ?")
        params.append(vdt_fim)
    # Nome
    if nome:
        filtros.append("LOWER(TRIM(t.razao)) LIKE ?")
        params.append(f"%{nome.strip().lower()}%")

    sql = """
    SELECT
        RECEBER.numero, 
        t.razao AS Nome, 
        RECEBER.valor_nf, 
        RECEBER.emissao, 
        RECEBER.vencimento, 
        RECEBER.valor, 
        RECEBER.pagamento, 
        RECEBER.valor_pago, 
        RECEBER.referente_a, 
        t.cgc,
        t.telefone, 
        t.fax, 
        t.fone_comercial, 
        t.endereco, 
        t.bairro, 
        t.cidade, 
        t.uf, 
        t.cep, 
        t.email, 
        t.obs, 
        RECEBER.conta
    FROM RECEBER 
    JOIN TITULAR t ON t.Codigo = RECEBER.TITULAR 
    """
    if filtros:
        sql += "\nWHERE " + " AND ".join(filtros)

    try:
        conn = get_firebird_conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        columns = [desc[0].lower() for desc in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()
        # Gera CSV
        output = StringIO()
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(columns)
        for row in rows:
            writer.writerow([tratar_valor(col, v) if tratar_valor(col, v) is not None else "" for col, v in zip(columns, row)])
        csv_data = output.getvalue()
        output.close()
        return Response(content=csv_data, media_type="text/csv", headers={
            "Content-Disposition": "attachment; filename=relatorio_cobranca.csv"
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "erro",
                "mensagem": f"Erro ao exportar CSV: {str(e)}"
            }
        )

app.include_router(router, prefix="/api/cobranca")