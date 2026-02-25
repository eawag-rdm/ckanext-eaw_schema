/* eaw_spatial_preview.js
 *
 * Shows a Leaflet map preview of the GeoJSON entered in the spatial field.
 * On blur, if the field contains valid GeoJSON, a Bootstrap 5 modal pops up
 * asking the user to confirm the location. The user can accept or swap
 * coordinates (lon/lat <-> lat/lon) if they appear reversed.
 */

"use strict";

ckan.module('eaw_spatial_preview', function ($) {
    var ALLOWED_TYPES = [
        'Point', 'MultiPoint', 'LineString',
        'MultiLineString', 'Polygon', 'MultiPolygon'
    ];

    return {
        initialize: function () {
            this.map = null;
            this.el.after($(this.modal_html));
            this.el.on('blur', this._onBlur.bind(this));

            var modalEl = document.getElementById('spatialPreviewModal');
            this.bsModal = new bootstrap.Modal(modalEl, {show: false});

            // Reinvalidate map size after the modal transition completes
            $(modalEl).on('shown.bs.modal', function () {
                if (this.map) {
                    this.map.invalidateSize();
                }
            }.bind(this));

            $('#spatialPreviewSwap').on('click', function () {
                this._swapAndUpdate();
                this.bsModal.hide();
            }.bind(this));
        },

        modal_html:
            '<div id="spatialPreviewModal" class="modal fade" tabindex="-1" aria-labelledby="spatialPreviewLabel" aria-hidden="true">' +
            '  <div class="modal-dialog" role="document">' +
            '    <div class="modal-content">' +
            '      <div class="modal-header">' +
            '        <h5 class="modal-title" id="spatialPreviewLabel">Spatial Preview</h5>' +
            '        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>' +
            '      </div>' +
            '      <div class="modal-body">' +
            '        <div id="spatialPreviewMap" style="width:100%;height:300px;"></div>' +
            '        <p class="mt-3"><strong>Is this the location you had in mind?</strong></p>' +
            '        <p class="text-muted" style="font-size:0.9em;">' +
            '          Note: GeoJSON uses [longitude,&nbsp;latitude] order, which is the opposite of ' +
            '          Google Maps [latitude,&nbsp;longitude]. If the location shown above seems wrong, ' +
            '          your coordinates may be swapped.' +
            '        </p>' +
            '      </div>' +
            '      <div class="modal-footer">' +
            '        <button type="button" class="btn btn-success" data-bs-dismiss="modal">Yes, looks correct</button>' +
            '        <button type="button" class="btn btn-warning" id="spatialPreviewSwap">No, swap coordinates</button>' +
            '      </div>' +
            '    </div>' +
            '  </div>' +
            '</div>',

        _onBlur: function () {
            var raw = this.el.val().trim();
            if (!raw) { return; }

            var geojson;
            try {
                geojson = JSON.parse(raw);
            } catch (e) {
                return;
            }

            // Only allow the geometry types the backend accepts
            if (ALLOWED_TYPES.indexOf(geojson.type) === -1) { return; }

            // Let Leaflet validate structure (coordinates, nesting, etc.)
            var layer;
            try {
                layer = L.geoJSON(geojson);
            } catch (e) {
                return;
            }
            if (layer.getLayers().length === 0) { return; }

            this._showMap(geojson, layer);
        },

        _showMap: function (geojson, layer) {
            // Destroy any previous map instance
            if (this.map) {
                this.map.remove();
                this.map = null;
            }

            this.bsModal.show();

            // Small delay to let the modal start rendering before creating the map
            setTimeout(function () {
                var map = L.map('spatialPreviewMap');
                this.map = map;

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; OpenStreetMap contributors',
                    maxZoom: 19
                }).addTo(map);

                layer.addTo(map);

                if (geojson.type === 'Point') {
                    var coords = geojson.coordinates;
                    map.setView([coords[1], coords[0]], 10);
                } else {
                    map.fitBounds(layer.getBounds(), {padding: [20, 20]});
                }

                map.invalidateSize();
            }.bind(this), 150);
        },

        _swapCoordinates: function (geojson) {
            var swapped = JSON.parse(JSON.stringify(geojson));
            swapped.coordinates = this._swapCoords(swapped.coordinates, swapped.type);
            return swapped;
        },

        _swapCoords: function (coords, type) {
            switch (type) {
                case 'Point':
                    return [coords[1], coords[0]];
                case 'MultiPoint':
                case 'LineString':
                    return coords.map(function (pair) {
                        return [pair[1], pair[0]];
                    });
                case 'Polygon':
                case 'MultiLineString':
                    return coords.map(function (ring) {
                        return ring.map(function (pair) {
                            return [pair[1], pair[0]];
                        });
                    });
                case 'MultiPolygon':
                    return coords.map(function (polygon) {
                        return polygon.map(function (ring) {
                            return ring.map(function (pair) {
                                return [pair[1], pair[0]];
                            });
                        });
                    });
                default:
                    return coords;
            }
        },

        _swapAndUpdate: function () {
            var raw = this.el.val().trim();
            if (!raw) { return; }

            try {
                var geojson = JSON.parse(raw);
                var swapped = this._swapCoordinates(geojson);
                this.el.val(JSON.stringify(swapped));
            } catch (e) {
                // Should not happen since we already validated, but be safe
                return;
            }
        }
    };
});
