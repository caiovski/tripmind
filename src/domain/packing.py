from typing import Any, Dict, List


def build_packing_checklist(
    weather_data: Dict[str, Any],
    days: int = 5,
    trip_type: str = "cidade"
) -> Dict[str, Any]:
    """Gera checklist inteligente de bagagem com base no clima e estilo de viagem.

    Regra de negócio pura: análise determinística sobre a previsão meteorológica.

    Args:
        weather_data (Dict[str, Any]): Dicionário com previsão do tempo.
        days (int): Duração da viagem em dias.
        trip_type (str): "cidade", "praia", "natureza" ou "neve".

    Returns:
        Dict[str, Any]: Categorias de itens e resumo de condições climáticas.
    """
    safe_days = max(int(days), 1)
    normalized_type = (trip_type or "cidade").lower().strip()
    forecast = weather_data.get("previsao", []) if isinstance(weather_data, dict) else []

    dias_chuva = sum(1 for d in forecast if d.get("prob_chuva_pct", 0) >= 40)
    dias_frio = sum(1 for d in forecast if d.get("temp_max_c", 30) <= 18)
    dias_calor = sum(1 for d in forecast if d.get("temp_max_c", 20) >= 28)
    temp_max = max((d.get("temp_max_c", 20) for d in forecast), default=22)
    temp_min = min((d.get("temp_min_c", 15) for d in forecast), default=15)
    is_internacional = weather_data.get("pais") not in (None, "BR")

    itens: Dict[str, List[str]] = {
        "documentos_e_financas": [
            "Passaporte válido e vistos" if is_internacional else "Documento de identidade oficial (RG/CNH)",
            "Cartão de crédito/débito internacional habilitado" if is_internacional else "Cartões bancários",
            "Dinheiro em espécie (moeda local)",
            "Seguro viagem internacional impresso" if is_internacional else "Cartão de saúde / plano",
            "Comprovantes de reserva e passagens digitais",
        ],
        "eletronicos": [
            "Smartphone e cabo carregador",
            "Carregador portátil (Power Bank homologado)",
            "Adaptador universal de tomadas" if is_internacional else "Adaptador padrão de tomadas",
            "Fones de ouvido com cancelamento de ruído",
        ],
        "higiene_e_cuidados": [
            "Kit essencial de higiene (escova, pasta, desodorante)",
            "Protetor solar FPS 50+" if temp_max >= 24 else "Protetor labial e hidratante facial",
            "Repelente de insetos (fórmula de longa duração)",
            "Farmacinha básica (analgésico, antialérgico, curativos)",
        ],
    }

    # Roupas por estilo de viagem
    roupas: List[str] = [
        f"Roupas íntimas ({safe_days + 2} conjuntos)",
        f"Meias ({safe_days + 1} pares)",
    ]

    if normalized_type == "praia":
        roupas.extend([
            "Roupas de banho (2 a 3 peças)",
            "Canga ou toalha de microfibra de secagem rápida",
            "Camisas leves de linho/algodão e shorts",
            "Chinelo, sandália e óculos de sol com proteção UV",
            "Chapéu ou boné com proteção",
        ])
    elif normalized_type == "neve":
        roupas.extend([
            "Segunda pele térmica (calça e blusa)",
            "Casaco corta-vento impermeável pesado",
            "Luvas térmicas impermeáveis e gorro de lã",
            "Cachecol térmico e meias de lã merino",
            "Botas impermeáveis com solado antiderrapante",
        ])
    elif normalized_type == "natureza":
        roupas.extend([
            "Roupas de tecido sintético respirável (dry-fit)",
            "Bota ou tênis específico para trilha (já amaciado)",
            "Jaqueta anorak impermeável e corta-vento",
            "Calça-bermuda destacável para trekking",
            "Mochila de ataque (20L) para caminhadas diurnas",
        ])
    else:  # cidade / urbano
        roupas.extend([
            "Roupas casuais e confortáveis para caminhada diurna",
            "Look sofisticado/social para jantares ou eventos noturnos",
            "Tênis casual muito confortável para andar bastante",
            "Jaqueta leve ou cardigã versátil",
        ])

    # Adições condicionais baseadas na previsão do tempo
    if dias_chuva > 0:
        roupas.append("Guarda-chuva compacto reforçado e capa de chuva leve")
    if dias_frio > 0:
        roupas.append("Casaco pesado e suéter extra de frio")
    if dias_calor > 0:
        roupas.append("Roupas frescas de algodão e boné")

    itens["vestuario"] = roupas
    itens["analise_metereologica"] = {
        "dias_com_previsao_chuva": dias_chuva,
        "dias_frios": dias_frio,
        "dias_quentes": dias_calor,
        "temperatura_maxima_prevista_c": temp_max,
        "temperatura_minima_prevista_c": temp_min,
    }

    return itens
