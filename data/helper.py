def build_where_clause(filters, date_range):
    clauses = []
    params = []

    if filters:
        for col, val in filters.items():
            clauses.append(f"{col} = ?")
            params.append(val)

    if date_range:
        clauses.append("Order_Date BETWEEN ? AND ?")
        params.extend([date_range["from"], date_range["to"]])

    if clauses:
        return " WHERE " + " AND ".join(clauses), tuple(params)

    return "", tuple()