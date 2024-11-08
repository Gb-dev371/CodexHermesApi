from fastapi import FastAPI, HTTPException
import json

app = FastAPI()

# Carregando os dados do JSON
with open("json/bribes/aerodrome/BribesData.json", "r") as file:
    bribes_data = json.load(file)

# Endpoint para obter a quantidade total de bribes de uma semana específica
@app.get("/total-bribes/{week}")
async def get_total_bribes(week: int):
    for week_data in bribes_data:
        if week_data["Week"] == week:
            return {"Week": week, "Total Bribes": week_data["Total Bribes"]}
    raise HTTPException(status_code=404, detail="Semana não encontrada")

# Endpoint para obter o valor de bribe de uma pool específica em uma semana específica
@app.get("/pool-bribe/{week}/{pool_address}")
async def get_pool_bribe(week: int, pool_address: str):
    for week_data in bribes_data:
        if week_data["Week"] == week:
            for pool in week_data["Pools Data"]:
                if pool["Pool Address"].lower() == pool_address.lower():
                    return {
                        "Week": week,
                        "Pool Address": pool_address,
                        "Pool Symbol": pool["Pool Symbol"],
                        "Bribe Dolar Value": pool["Bribe Dolar Value"]
                    }
            raise HTTPException(status_code=404, detail="Pool não encontrada na semana especificada")
    raise HTTPException(status_code=404, detail="Semana não encontrada")

# Endpoint para listar todas as semanas disponíveis
@app.get("/weeks")
async def get_weeks():
    weeks = [week_data["Week"] for week_data in bribes_data]
    return {"Available Weeks": weeks}

# Endpoint para listar todas as pools de uma semana específica
@app.get("/pools/{week}")
async def get_pools(week: int):
    for week_data in bribes_data:
        if week_data["Week"] == week:
            pools = [{"Pool Symbol": pool["Pool Symbol"], "Pool Address": pool["Pool Address"]} for pool in week_data["Pools Data"]]
            return {"Week": week, "Pools": pools}
    raise HTTPException(status_code=404, detail="Semana não encontrada")
