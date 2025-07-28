#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odoo_api.py

Cliente ligero para consumir la REST API de Odoo (módulo jeepsleep/api-odoo).
"""

import json
from typing import Any, Dict, List, Optional, Union

import requests

from config.config import get_settings


class OdooAPI:
    """Cliente REST para la API de Odoo (jeepsleep/api-odoo)."""

    def __init__(self, base_url: str, db: str, login: str, password: str) -> None:
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        })
        self.db = db
        self.login = login
        self.password = password
        self._authenticate()

    def _authenticate(self) -> None:
        """Se autentica contra /web/session/authenticate y guarda la cookie."""
        url = f"{self.base_url}/web/session/authenticate"
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': self.db,
                'login': self.login,
                'password': self.password,
            }
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()

        try:
            data = resp.json()
        except ValueError:
            raise RuntimeError("Autenticación: la respuesta no es JSON")

        if 'error' in data:
            raise RuntimeError(f"Error en autenticación: {data['error']}")

        uid = data.get('result', {}).get('uid')
        if not uid:
            raise RuntimeError(f"Autenticación fallida: {data}")

    def get(
        self,
        model: str,
        query: Optional[Union[str, List[str]]] = None,
        filters: Optional[List[List[Any]]] = None,
        page_size: Optional[int] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        order: Optional[str] = None,
    ) -> Dict[str, Any]:
        """GET /api/{model}/"""
        url = f"{self.base_url}/api/{model}/"
        params: Dict[str, Any] = {}

        if query:
            params['query'] = f"{{{','.join(query)}}}" if isinstance(query, list) else query
        if filters:
            params['filter'] = json.dumps(filters)
        if page_size:
            params['page_size'] = page_size
        if page:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        if order:
            params['order'] = order

        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_single(
        self,
        model: str,
        record_id: Union[int, str],
        query: Optional[Union[str, List[str]]] = None,
    ) -> Dict[str, Any]:
        """GET /api/{model}/{id}/"""
        url = f"{self.base_url}/api/{model}/{record_id}/"
        params = {}
        if query:
            params['query'] = f"{{{','.join(query)}}}" if isinstance(query, list) else query
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def create(
        self,
        model: str,
        data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> int:
        """POST /api/{model}/"""
        url = f"{self.base_url}/api/{model}/"
        body = {'params': {'data': data}}
        if context:
            body['params']['context'] = context

        resp = self.session.post(url, json=body)
        resp.raise_for_status()
        resp_json = resp.json()

        if 'error' in resp_json:
            raise RuntimeError(f"Error al crear en {model}: {resp_json['error']['message']}")

        new_id = resp_json.get('result')
        if not isinstance(new_id, int):
            raise RuntimeError(f"Respuesta inesperada al crear en {model}: {resp_json}")
        return new_id

    def update(
        self,
        model: str,
        filters: List[List[Any]],
        data: Dict[str, Any],
    ) -> bool:
        """PUT /api/{model}/"""
        url = f"{self.base_url}/api/{model}/"
        body = {'params': {'filter': filters, 'data': data}}
        resp = self.session.put(url, json=body)
        resp.raise_for_status()
        return bool(resp.json().get('result', False))

    @classmethod
    def from_config(cls) -> "OdooAPI":
        """Create OdooAPI instance using config settings."""
        settings = get_settings()
        base_url, db, login, password = settings.get_odoo_params()
        return cls(base_url, db, login, password) 