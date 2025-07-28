FROM odoo:18

USER root
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/yezyilomo/odoo-rest-api /mnt/extra-addons/odoo-rest-api
RUN chown -R odoo:odoo /mnt/extra-addons
RUN pip install --break-system-packages -r /mnt/extra-addons/odoo-rest-api/requirements.txt --no-cache-dir
RUN mkdir -p /var/lib/odoo/.local/share/Odoo/sessions \
    && chown -R odoo:odoo /var/lib/odoo/.local

USER odoo
