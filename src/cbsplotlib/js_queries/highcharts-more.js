/*
 Highcharts JS v7.0.3 (2019-02-06)

 (c) 2009-2018 Torstein Honsi

 License: www.highcharts.com/license
*/
(function(z) {
    "object" === typeof module && module.exports ? (z["default"] = z,
    module.exports = z) : "function" === typeof define && define.amd ? define(function() {
        return z
    }) : z("undefined" !== typeof Highcharts ? Highcharts : void 0)
}
)(function(z) {
    (function(a) {
        function w(a, b) {
            this.init(a, b)
        }
        var x = a.CenteredSeriesMixin
          , g = a.extend
          , h = a.merge
          , u = a.splat;
        g(w.prototype, {
            coll: "pane",
            init: function(a, b) {
                this.chart = b;
                this.background = [];
                b.pane.push(this);
                this.setOptions(a)
            },
            setOptions: function(a) {
                this.options = h(this.defaultOptions, this.chart.angular ? {
                    background: {}
                } : void 0, a)
            },
            render: function() {
                var a = this.options
                  , b = this.options.background
                  , d = this.chart.renderer;
                this.group || (this.group = d.g("pane-group").attr({
                    zIndex: a.zIndex || 0
                }).add());
                this.updateCenter();
                if (b)
                    for (b = u(b),
                    a = Math.max(b.length, this.background.length || 0),
                    d = 0; d < a; d++)
                        b[d] && this.axis ? this.renderBackground(h(this.defaultBackgroundOptions, b[d]), d) : this.background[d] && (this.background[d] = this.background[d].destroy(),
                        this.background.splice(d, 1))
            },
            renderBackground: function(a, b) {
                var d = "animate"
                  , e = {
                    "class": "highcharts-pane " + (a.className || "")
                };
                this.chart.styledMode || g(e, {
                    fill: a.backgroundColor,
                    stroke: a.borderColor,
                    "stroke-width": a.borderWidth
                });
                this.background[b] || (this.background[b] = this.chart.renderer.path().add(this.group),
                d = "attr");
                this.background[b][d]({
                    d: this.axis.getPlotBandPath(a.from, a.to, a)
                }).attr(e)
            },
            defaultOptions: {
                center: ["50%", "50%"],
                size: "85%",
                startAngle: 0
            },
            defaultBackgroundOptions: {
                shape: "circle",
                borderWidth: 1,
                borderColor: "#cccccc",
                backgroundColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [[0, "#ffffff"], [1, "#e6e6e6"]]
                },
                from: -Number.MAX_VALUE,
                innerRadius: 0,
                to: Number.MAX_VALUE,
                outerRadius: "105%"
            },
            updateCenter: function(a) {
                this.center = (a || this.axis || {}).center = x.getCenter.call(this)
            },
            update: function(a, b) {
                h(!0, this.options, a);
                this.setOptions(this.options);
                this.render();
                this.chart.axes.forEach(function(a) {
                    a.pane === this && (a.pane = null,
                    a.update({}, b))
                }, this)
            }
        });
        a.Pane = w
    }
    )(z);
    (function(a) {
        var w = a.addEvent, x = a.Axis, g = a.extend, h = a.merge, u = a.noop, p = a.pick, b = a.pInt, d = a.Tick, e = a.wrap, c = a.correctFloat, q, t, v = x.prototype, m = d.prototype;
        a.radialAxisExtended || (a.radialAxisExtended = !0,
        q = {
            getOffset: u,
            redraw: function() {
                this.isDirty = !1
            },
            render: function() {
                this.isDirty = !1
            },
            setScale: u,
            setCategories: u,
            setTitle: u
        },
        t = {
            defaultRadialGaugeOptions: {
                labels: {
                    align: "center",
                    x: 0,
                    y: null
                },
                minorGridLineWidth: 0,
                minorTickInterval: "auto",
                minorTickLength: 10,
                minorTickPosition: "inside",
                minorTickWidth: 1,
                tickLength: 10,
                tickPosition: "inside",
                tickWidth: 2,
                title: {
                    rotation: 0
                },
                zIndex: 2
            },
            defaultRadialXOptions: {
                gridLineWidth: 1,
                labels: {
                    align: null,
                    distance: 15,
                    x: 0,
                    y: null,
                    style: {
                        textOverflow: "none"
                    }
                },
                maxPadding: 0,
                minPadding: 0,
                showLastLabel: !1,
                tickLength: 0
            },
            defaultRadialYOptions: {
                gridLineInterpolation: "circle",
                labels: {
                    align: "right",
                    x: -3,
                    y: -2
                },
                showLastLabel: !1,
                title: {
                    x: 4,
                    text: null,
                    rotation: 90
                }
            },
            setOptions: function(l) {
                l = this.options = h(this.defaultOptions, this.defaultRadialOptions, l);
                l.plotBands || (l.plotBands = []);
                a.fireEvent(this, "afterSetOptions")
            },
            getOffset: function() {
                v.getOffset.call(this);
                this.chart.axisOffset[this.side] = 0
            },
            getLinePath: function(l, n) {
                l = this.center;
                var f = this.chart
                  , k = p(n, l[2] / 2 - this.offset);
                this.isCircular || void 0 !== n ? (n = this.chart.renderer.symbols.arc(this.left + l[0], this.top + l[1], k, k, {
                    start: this.startAngleRad,
                    end: this.endAngleRad,
                    open: !0,
                    innerR: 0
                }),
                n.xBounds = [this.left + l[0]],
                n.yBounds = [this.top + l[1] - k]) : (n = this.postTranslate(this.angleRad, k),
                n = ["M", l[0] + f.plotLeft, l[1] + f.plotTop, "L", n.x, n.y]);
                return n
            },
            setAxisTranslation: function() {
                v.setAxisTranslation.call(this);
                this.center && (this.transA = this.isCircular ? (this.endAngleRad - this.startAngleRad) / (this.max - this.min || 1) : this.center[2] / 2 / (this.max - this.min || 1),
                this.minPixelPadding = this.isXAxis ? this.transA * this.minPointOffset : 0)
            },
            beforeSetTickPositions: function() {
                if (this.autoConnect = this.isCircular && void 0 === p(this.userMax, this.options.max) && c(this.endAngleRad - this.startAngleRad) === c(2 * Math.PI))
                    this.max += this.categories && 1 || this.pointRange || this.closestPointRange || 0
            },
            setAxisSize: function() {
                v.setAxisSize.call(this);
                this.isRadial && (this.pane.updateCenter(this),
                this.isCircular && (this.sector = this.endAngleRad - this.startAngleRad),
                this.len = this.width = this.height = this.center[2] * p(this.sector, 1) / 2)
            },
            getPosition: function(l, n) {
                return this.postTranslate(this.isCircular ? this.translate(l) : this.angleRad, p(this.isCircular ? n : this.translate(l), this.center[2] / 2) - this.offset)
            },
            postTranslate: function(l, n) {
                var f = this.chart
                  , k = this.center;
                l = this.startAngleRad + l;
                return {
                    x: f.plotLeft + k[0] + Math.cos(l) * n,
                    y: f.plotTop + k[1] + Math.sin(l) * n
                }
            },
            getPlotBandPath: function(l, n, f) {
                var k = this.center, c = this.startAngleRad, m = k[2] / 2, a = [p(f.outerRadius, "100%"), f.innerRadius, p(f.thickness, 10)], e = Math.min(this.offset, 0), v = /%$/, d, q = this.isCircular;
                "polygon" === this.options.gridLineInterpolation ? k = this.getPlotLinePath(l).concat(this.getPlotLinePath(n, !0)) : (l = Math.max(l, this.min),
                n = Math.min(n, this.max),
                q || (a[0] = this.translate(l),
                a[1] = this.translate(n)),
                a = a.map(function(f) {
                    v.test(f) && (f = b(f, 10) * m / 100);
                    return f
                }),
                "circle" !== f.shape && q ? (l = c + this.translate(l),
                n = c + this.translate(n)) : (l = -Math.PI / 2,
                n = 1.5 * Math.PI,
                d = !0),
                a[0] -= e,
                a[2] -= e,
                k = this.chart.renderer.symbols.arc(this.left + k[0], this.top + k[1], a[0], a[0], {
                    start: Math.min(l, n),
                    end: Math.max(l, n),
                    innerR: p(a[1], a[0] - a[2]),
                    open: d
                }));
                return k
            },
            getPlotLinePath: function(l, c) {
                var f = this, k = f.center, n = f.chart, a = f.getPosition(l), b, m, e;
                f.isCircular ? e = ["M", k[0] + n.plotLeft, k[1] + n.plotTop, "L", a.x, a.y] : "circle" === f.options.gridLineInterpolation ? (l = f.translate(l),
                e = f.getLinePath(0, l)) : (n.xAxis.forEach(function(k) {
                    k.pane === f.pane && (b = k)
                }),
                e = [],
                l = f.translate(l),
                k = b.tickPositions,
                b.autoConnect && (k = k.concat([k[0]])),
                c && (k = [].concat(k).reverse()),
                k.forEach(function(f, k) {
                    m = b.getPosition(f, l);
                    e.push(k ? "L" : "M", m.x, m.y)
                }));
                return e
            },
            getTitlePosition: function() {
                var l = this.center
                  , c = this.chart
                  , f = this.options.title;
                return {
                    x: c.plotLeft + l[0] + (f.x || 0),
                    y: c.plotTop + l[1] - {
                        high: .5,
                        middle: .25,
                        low: 0
                    }[f.align] * l[2] + (f.y || 0)
                }
            }
        },
        w(x, "init", function(l) {
            var c = this, f = this.chart, k = f.angular, a = f.polar, b = this.isXAxis, m = k && b, e, v = f.options;
            l = l.userOptions.pane || 0;
            l = this.pane = f.pane && f.pane[l];
            if (k) {
                if (g(this, m ? q : t),
                e = !b)
                    this.defaultRadialOptions = this.defaultRadialGaugeOptions
            } else
                a && (g(this, t),
                this.defaultRadialOptions = (e = b) ? this.defaultRadialXOptions : h(this.defaultYAxisOptions, this.defaultRadialYOptions));
            k || a ? (this.isRadial = !0,
            f.inverted = !1,
            v.chart.zoomType = null,
            f.labelCollectors.push(function() {
                if (c.isRadial && c.tickPositions && !0 !== c.options.labels.allowOverlap)
                    return c.tickPositions.map(function(f) {
                        return c.ticks[f] && c.ticks[f].label
                    }).filter(function(f) {
                        return !!f
                    })
            })) : this.isRadial = !1;
            l && e && (l.axis = this);
            this.isCircular = e
        }),
        w(x, "afterInit", function() {
            var c = this.chart
              , a = this.options
              , f = this.pane
              , k = f && f.options;
            c.angular && this.isXAxis || !f || !c.angular && !c.polar || (this.angleRad = (a.angle || 0) * Math.PI / 180,
            this.startAngleRad = (k.startAngle - 90) * Math.PI / 180,
            this.endAngleRad = (p(k.endAngle, k.startAngle + 360) - 90) * Math.PI / 180,
            this.offset = a.offset || 0)
        }),
        w(x, "autoLabelAlign", function(c) {
            this.isRadial && (c.align = void 0,
            c.preventDefault())
        }),
        w(d, "afterGetPosition", function(c) {
            this.axis.getPosition && g(c.pos, this.axis.getPosition(this.pos))
        }),
        w(d, "afterGetLabelPosition", function(c) {
            var a = this.axis, f = this.label, k = a.options.labels, l = k.y, b, m = 20, e = k.align, v = (a.translate(this.pos) + a.startAngleRad + Math.PI / 2) / Math.PI * 180 % 360;
            a.isRadial && (b = a.getPosition(this.pos, a.center[2] / 2 + p(k.distance, -25)),
            "auto" === k.rotation ? f.attr({
                rotation: v
            }) : null === l && (l = a.chart.renderer.fontMetrics(f.styles && f.styles.fontSize).b - f.getBBox().height / 2),
            null === e && (a.isCircular ? (this.label.getBBox().width > a.len * a.tickInterval / (a.max - a.min) && (m = 0),
            e = v > m && v < 180 - m ? "left" : v > 180 + m && v < 360 - m ? "right" : "center") : e = "center",
            f.attr({
                align: e
            })),
            c.pos.x = b.x + k.x,
            c.pos.y = b.y + l)
        }),
        e(m, "getMarkPath", function(c, a, f, k, b, m, e) {
            var l = this.axis;
            l.isRadial ? (c = l.getPosition(this.pos, l.center[2] / 2 + k),
            a = ["M", a, f, "L", c.x, c.y]) : a = c.call(this, a, f, k, b, m, e);
            return a
        }))
    }
    )(z);
    (function(a) {
        var w = a.pick
          , x = a.extend
          , g = a.isArray
          , h = a.defined
          , u = a.seriesType
          , p = a.seriesTypes
          , b = a.Series.prototype
          , d = a.Point.prototype;
        u("arearange", "area", {
            lineWidth: 1,
            threshold: null,
            tooltip: {
                pointFormat: '\x3cspan style\x3d"color:{series.color}"\x3e\u25cf\x3c/span\x3e {series.name}: \x3cb\x3e{point.low}\x3c/b\x3e - \x3cb\x3e{point.high}\x3c/b\x3e\x3cbr/\x3e'
            },
            trackByArea: !0,
            dataLabels: {
                align: null,
                verticalAlign: null,
                xLow: 0,
                xHigh: 0,
                yLow: 0,
                yHigh: 0
            }
        }, {
            pointArrayMap: ["low", "high"],
            toYData: function(a) {
                return [a.low, a.high]
            },
            pointValKey: "low",
            deferTranslatePolar: !0,
            highToXY: function(a) {
                var c = this.chart
                  , b = this.xAxis.postTranslate(a.rectPlotX, this.yAxis.len - a.plotHigh);
                a.plotHighX = b.x - c.plotLeft;
                a.plotHigh = b.y - c.plotTop;
                a.plotLowX = a.plotX
            },
            translate: function() {
                var a = this
                  , c = a.yAxis
                  , b = !!a.modifyValue;
                p.area.prototype.translate.apply(a);
                a.points.forEach(function(e) {
                    var v = e.low
                      , m = e.high
                      , l = e.plotY;
                    null === m || null === v ? (e.isNull = !0,
                    e.plotY = null) : (e.plotLow = l,
                    e.plotHigh = c.translate(b ? a.modifyValue(m, e) : m, 0, 1, 0, 1),
                    b && (e.yBottom = e.plotHigh))
                });
                this.chart.polar && this.points.forEach(function(c) {
                    a.highToXY(c);
                    c.tooltipPos = [(c.plotHighX + c.plotLowX) / 2, (c.plotHigh + c.plotLow) / 2]
                })
            },
            getGraphPath: function(a) {
                var c = [], b = [], e, v = p.area.prototype.getGraphPath, m, l, n;
                n = this.options;
                var f = this.chart.polar && !1 !== n.connectEnds
                  , k = n.connectNulls
                  , d = n.step;
                a = a || this.points;
                for (e = a.length; e--; )
                    m = a[e],
                    m.isNull || f || k || a[e + 1] && !a[e + 1].isNull || b.push({
                        plotX: m.plotX,
                        plotY: m.plotY,
                        doCurve: !1
                    }),
                    l = {
                        polarPlotY: m.polarPlotY,
                        rectPlotX: m.rectPlotX,
                        yBottom: m.yBottom,
                        plotX: w(m.plotHighX, m.plotX),
                        plotY: m.plotHigh,
                        isNull: m.isNull
                    },
                    b.push(l),
                    c.push(l),
                    m.isNull || f || k || a[e - 1] && !a[e - 1].isNull || b.push({
                        plotX: m.plotX,
                        plotY: m.plotY,
                        doCurve: !1
                    });
                a = v.call(this, a);
                d && (!0 === d && (d = "left"),
                n.step = {
                    left: "right",
                    center: "center",
                    right: "left"
                }[d]);
                c = v.call(this, c);
                b = v.call(this, b);
                n.step = d;
                n = [].concat(a, c);
                this.chart.polar || "M" !== b[0] || (b[0] = "L");
                this.graphPath = n;
                this.areaPath = a.concat(b);
                n.isArea = !0;
                n.xMap = a.xMap;
                this.areaPath.xMap = a.xMap;
                return n
            },
            drawDataLabels: function() {
                var a = this.points, c = a.length, d, h = [], v = this.options.dataLabels, m, l, n = this.chart.inverted, f, k;
                g(v) ? 1 < v.length ? (f = v[0],
                k = v[1]) : (f = v[0],
                k = {
                    enabled: !1
                }) : (f = x({}, v),
                f.x = v.xHigh,
                f.y = v.yHigh,
                k = x({}, v),
                k.x = v.xLow,
                k.y = v.yLow);
                if (f.enabled || this._hasPointLabels) {
                    for (d = c; d--; )
                        if (m = a[d])
                            l = f.inside ? m.plotHigh < m.plotLow : m.plotHigh > m.plotLow,
                            m.y = m.high,
                            m._plotY = m.plotY,
                            m.plotY = m.plotHigh,
                            h[d] = m.dataLabel,
                            m.dataLabel = m.dataLabelUpper,
                            m.below = l,
                            n ? f.align || (f.align = l ? "right" : "left") : f.verticalAlign || (f.verticalAlign = l ? "top" : "bottom");
                    this.options.dataLabels = f;
                    b.drawDataLabels && b.drawDataLabels.apply(this, arguments);
                    for (d = c; d--; )
                        if (m = a[d])
                            m.dataLabelUpper = m.dataLabel,
                            m.dataLabel = h[d],
                            delete m.dataLabels,
                            m.y = m.low,
                            m.plotY = m._plotY
                }
                if (k.enabled || this._hasPointLabels) {
                    for (d = c; d--; )
                        if (m = a[d])
                            l = k.inside ? m.plotHigh < m.plotLow : m.plotHigh > m.plotLow,
                            m.below = !l,
                            n ? k.align || (k.align = l ? "left" : "right") : k.verticalAlign || (k.verticalAlign = l ? "bottom" : "top");
                    this.options.dataLabels = k;
                    b.drawDataLabels && b.drawDataLabels.apply(this, arguments)
                }
                if (f.enabled)
                    for (d = c; d--; )
                        if (m = a[d])
                            m.dataLabels = [m.dataLabelUpper, m.dataLabel].filter(function(f) {
                                return !!f
                            });
                this.options.dataLabels = v
            },
            alignDataLabel: function() {
                p.column.prototype.alignDataLabel.apply(this, arguments)
            },
            drawPoints: function() {
                var d = this.points.length, c, q;
                b.drawPoints.apply(this, arguments);
                for (q = 0; q < d; )
                    c = this.points[q],
                    c.origProps = {
                        plotY: c.plotY,
                        plotX: c.plotX,
                        isInside: c.isInside,
                        negative: c.negative,
                        zone: c.zone,
                        y: c.y
                    },
                    c.lowerGraphic = c.graphic,
                    c.graphic = c.upperGraphic,
                    c.plotY = c.plotHigh,
                    h(c.plotHighX) && (c.plotX = c.plotHighX),
                    c.y = c.high,
                    c.negative = c.high < (this.options.threshold || 0),
                    c.zone = this.zones.length && c.getZone(),
                    this.chart.polar || (c.isInside = c.isTopInside = void 0 !== c.plotY && 0 <= c.plotY && c.plotY <= this.yAxis.len && 0 <= c.plotX && c.plotX <= this.xAxis.len),
                    q++;
                b.drawPoints.apply(this, arguments);
                for (q = 0; q < d; )
                    c = this.points[q],
                    c.upperGraphic = c.graphic,
                    c.graphic = c.lowerGraphic,
                    a.extend(c, c.origProps),
                    delete c.origProps,
                    q++
            },
            setStackedPoints: a.noop
        }, {
            setState: function() {
                var a = this.state
                  , c = this.series
                  , b = c.chart.polar;
                h(this.plotHigh) || (this.plotHigh = c.yAxis.toPixels(this.high, !0));
                h(this.plotLow) || (this.plotLow = this.plotY = c.yAxis.toPixels(this.low, !0));
                c.stateMarkerGraphic && (c.lowerStateMarkerGraphic = c.stateMarkerGraphic,
                c.stateMarkerGraphic = c.upperStateMarkerGraphic);
                this.graphic = this.upperGraphic;
                this.plotY = this.plotHigh;
                b && (this.plotX = this.plotHighX);
                d.setState.apply(this, arguments);
                this.state = a;
                this.plotY = this.plotLow;
                this.graphic = this.lowerGraphic;
                b && (this.plotX = this.plotLowX);
                c.stateMarkerGraphic && (c.upperStateMarkerGraphic = c.stateMarkerGraphic,
                c.stateMarkerGraphic = c.lowerStateMarkerGraphic,
                c.lowerStateMarkerGraphic = void 0);
                d.setState.apply(this, arguments)
            },
            haloPath: function() {
                var a = this.series.chart.polar
                  , c = [];
                this.plotY = this.plotLow;
                a && (this.plotX = this.plotLowX);
                this.isInside && (c = d.haloPath.apply(this, arguments));
                this.plotY = this.plotHigh;
                a && (this.plotX = this.plotHighX);
                this.isTopInside && (c = c.concat(d.haloPath.apply(this, arguments)));
                return c
            },
            destroyElements: function() {
                ["lowerGraphic", "upperGraphic"].forEach(function(a) {
                    this[a] && (this[a] = this[a].destroy())
                }, this);
                this.graphic = null;
                return d.destroyElements.apply(this, arguments)
            }
        })
    }
    )(z);
    (function(a) {
        var w = a.seriesType;
        w("areasplinerange", "arearange", null, {
            getPointSpline: a.seriesTypes.spline.prototype.getPointSpline
        })
    }
    )(z);
    (function(a) {
        var w = a.defaultPlotOptions
          , x = a.merge
          , g = a.noop
          , h = a.pick
          , u = a.seriesType
          , p = a.seriesTypes.column.prototype;
        u("columnrange", "arearange", x(w.column, w.arearange, {
            pointRange: null,
            marker: null,
            states: {
                hover: {
                    halo: !1
                }
            }
        }), {
            translate: function() {
                var a = this, d = a.yAxis, e = a.xAxis, c = e.startAngleRad, q, t = a.chart, v = a.xAxis.isRadial, m = Math.max(t.chartWidth, t.chartHeight) + 999, l;
                p.translate.apply(a);
                a.points.forEach(function(b) {
                    var f = b.shapeArgs, k = a.options.minPointLength, n, y;
                    b.plotHigh = l = Math.min(Math.max(-m, d.translate(b.high, 0, 1, 0, 1)), m);
                    b.plotLow = Math.min(Math.max(-m, b.plotY), m);
                    y = l;
                    n = h(b.rectPlotY, b.plotY) - l;
                    Math.abs(n) < k ? (k -= n,
                    n += k,
                    y -= k / 2) : 0 > n && (n *= -1,
                    y -= n);
                    v ? (q = b.barX + c,
                    b.shapeType = "path",
                    b.shapeArgs = {
                        d: a.polarArc(y + n, y, q, q + b.pointWidth)
                    }) : (f.height = n,
                    f.y = y,
                    b.tooltipPos = t.inverted ? [d.len + d.pos - t.plotLeft - y - n / 2, e.len + e.pos - t.plotTop - f.x - f.width / 2, n] : [e.left - t.plotLeft + f.x + f.width / 2, d.pos - t.plotTop + y + n / 2, n])
                })
            },
            directTouch: !0,
            trackerGroups: ["group", "dataLabelsGroup"],
            drawGraph: g,
            getSymbol: g,
            crispCol: function() {
                return p.crispCol.apply(this, arguments)
            },
            drawPoints: function() {
                return p.drawPoints.apply(this, arguments)
            },
            drawTracker: function() {
                return p.drawTracker.apply(this, arguments)
            },
            getColumnMetrics: function() {
                return p.getColumnMetrics.apply(this, arguments)
            },
            pointAttribs: function() {
                return p.pointAttribs.apply(this, arguments)
            },
            animate: function() {
                return p.animate.apply(this, arguments)
            },
            polarArc: function() {
                return p.polarArc.apply(this, arguments)
            },
            translate3dPoints: function() {
                return p.translate3dPoints.apply(this, arguments)
            },
            translate3dShapes: function() {
                return p.translate3dShapes.apply(this, arguments)
            }
        }, {
            setState: p.pointClass.prototype.setState
        })
    }
    )(z);
    (function(a) {
        var w = a.pick
          , x = a.seriesType
          , g = a.seriesTypes.column.prototype;
        x("columnpyramid", "column", {}, {
            translate: function() {
                var a = this
                  , u = a.chart
                  , p = a.options
                  , b = a.dense = 2 > a.closestPointRange * a.xAxis.transA
                  , b = a.borderWidth = w(p.borderWidth, b ? 0 : 1)
                  , d = a.yAxis
                  , e = p.threshold
                  , c = a.translatedThreshold = d.getThreshold(e)
                  , q = w(p.minPointLength, 5)
                  , t = a.getColumnMetrics()
                  , v = t.width
                  , m = a.barW = Math.max(v, 1 + 2 * b)
                  , l = a.pointXOffset = t.offset;
                u.inverted && (c -= .5);
                p.pointPadding && (m = Math.ceil(m));
                g.translate.apply(a);
                a.points.forEach(function(b) {
                    var f = w(b.yBottom, c), k = 999 + Math.abs(f), n = Math.min(Math.max(-k, b.plotY), d.len + k), k = b.plotX + l, y = m / 2, B = Math.min(n, f), f = Math.max(n, f) - B, h, r, t, g, x, D;
                    b.barX = k;
                    b.pointWidth = v;
                    b.tooltipPos = u.inverted ? [d.len + d.pos - u.plotLeft - n, a.xAxis.len - k - y, f] : [k + y, n + d.pos - u.plotTop, f];
                    n = e + (b.total || b.y);
                    "percent" === p.stacking && (n = e + (0 > b.y) ? -100 : 100);
                    n = d.toPixels(n, !0);
                    h = u.plotHeight - n - (u.plotHeight - c);
                    r = y * (B - n) / h;
                    t = y * (B + f - n) / h;
                    h = k - r + y;
                    r = k + r + y;
                    g = k + t + y;
                    t = k - t + y;
                    x = B - q;
                    D = B + f;
                    0 > b.y && (x = B,
                    D = B + f + q);
                    u.inverted && (g = u.plotWidth - B,
                    h = n - (u.plotWidth - c),
                    r = y * (n - g) / h,
                    t = y * (n - (g - f)) / h,
                    h = k + y + r,
                    r = h - 2 * r,
                    g = k - t + y,
                    t = k + t + y,
                    x = B,
                    D = B + f - q,
                    0 > b.y && (D = B + f + q));
                    b.shapeType = "path";
                    b.shapeArgs = {
                        x: h,
                        y: x,
                        width: r - h,
                        height: f,
                        d: ["M", h, x, "L", r, x, g, D, t, D, "Z"]
                    }
                })
            }
        })
    }
    )(z);
    (function(a) {
        var w = a.isNumber
          , x = a.merge
          , g = a.pick
          , h = a.pInt
          , u = a.Series
          , p = a.seriesType
          , b = a.TrackerMixin;
        p("gauge", "line", {
            dataLabels: {
                enabled: !0,
                defer: !1,
                y: 15,
                borderRadius: 3,
                crop: !1,
                verticalAlign: "top",
                zIndex: 2,
                borderWidth: 1,
                borderColor: "#cccccc"
            },
            dial: {},
            pivot: {},
            tooltip: {
                headerFormat: ""
            },
            showInLegend: !1
        }, {
            angular: !0,
            directTouch: !0,
            drawGraph: a.noop,
            fixedBox: !0,
            forceDL: !0,
            noSharedTooltip: !0,
            trackerGroups: ["group", "dataLabelsGroup"],
            translate: function() {
                var a = this.yAxis
                  , b = this.options
                  , c = a.center;
                this.generatePoints();
                this.points.forEach(function(d) {
                    var e = x(b.dial, d.dial)
                      , v = h(g(e.radius, 80)) * c[2] / 200
                      , m = h(g(e.baseLength, 70)) * v / 100
                      , l = h(g(e.rearLength, 10)) * v / 100
                      , n = e.baseWidth || 3
                      , f = e.topWidth || 1
                      , k = b.overshoot
                      , C = a.startAngleRad + a.translate(d.y, null, null, null, !0);
                    w(k) ? (k = k / 180 * Math.PI,
                    C = Math.max(a.startAngleRad - k, Math.min(a.endAngleRad + k, C))) : !1 === b.wrap && (C = Math.max(a.startAngleRad, Math.min(a.endAngleRad, C)));
                    C = 180 * C / Math.PI;
                    d.shapeType = "path";
                    d.shapeArgs = {
                        d: e.path || ["M", -l, -n / 2, "L", m, -n / 2, v, -f / 2, v, f / 2, m, n / 2, -l, n / 2, "z"],
                        translateX: c[0],
                        translateY: c[1],
                        rotation: C
                    };
                    d.plotX = c[0];
                    d.plotY = c[1]
                })
            },
            drawPoints: function() {
                var a = this
                  , b = a.chart
                  , c = a.yAxis.center
                  , q = a.pivot
                  , h = a.options
                  , v = h.pivot
                  , m = b.renderer;
                a.points.forEach(function(c) {
                    var l = c.graphic
                      , f = c.shapeArgs
                      , k = f.d
                      , d = x(h.dial, c.dial);
                    l ? (l.animate(f),
                    f.d = k) : (c.graphic = m[c.shapeType](f).attr({
                        rotation: f.rotation,
                        zIndex: 1
                    }).addClass("highcharts-dial").add(a.group),
                    b.styledMode || c.graphic.attr({
                        stroke: d.borderColor || "none",
                        "stroke-width": d.borderWidth || 0,
                        fill: d.backgroundColor || "#000000"
                    }))
                });
                q ? q.animate({
                    translateX: c[0],
                    translateY: c[1]
                }) : (a.pivot = m.circle(0, 0, g(v.radius, 5)).attr({
                    zIndex: 2
                }).addClass("highcharts-pivot").translate(c[0], c[1]).add(a.group),
                b.styledMode || a.pivot.attr({
                    "stroke-width": v.borderWidth || 0,
                    stroke: v.borderColor || "#cccccc",
                    fill: v.backgroundColor || "#000000"
                }))
            },
            animate: function(a) {
                var b = this;
                a || (b.points.forEach(function(a) {
                    var c = a.graphic;
                    c && (c.attr({
                        rotation: 180 * b.yAxis.startAngleRad / Math.PI
                    }),
                    c.animate({
                        rotation: a.shapeArgs.rotation
                    }, b.options.animation))
                }),
                b.animate = null)
            },
            render: function() {
                this.group = this.plotGroup("group", "series", this.visible ? "visible" : "hidden", this.options.zIndex, this.chart.seriesGroup);
                u.prototype.render.call(this);
                this.group.clip(this.chart.clipRect)
            },
            setData: function(a, b) {
                u.prototype.setData.call(this, a, !1);
                this.processData();
                this.generatePoints();
                g(b, !0) && this.chart.redraw()
            },
            drawTracker: b && b.drawTrackerPoint
        }, {
            setState: function(a) {
                this.state = a
            }
        })
    }
    )(z);
    (function(a) {
        var w = a.noop
          , x = a.pick
          , g = a.seriesType
          , h = a.seriesTypes;
        g("boxplot", "column", {
            threshold: null,
            tooltip: {
                pointFormat: '\x3cspan style\x3d"color:{point.color}"\x3e\u25cf\x3c/span\x3e \x3cb\x3e {series.name}\x3c/b\x3e\x3cbr/\x3eMaximum: {point.high}\x3cbr/\x3eUpper quartile: {point.q3}\x3cbr/\x3eMedian: {point.median}\x3cbr/\x3eLower quartile: {point.q1}\x3cbr/\x3eMinimum: {point.low}\x3cbr/\x3e'
            },
            whiskerLength: "50%",
            fillColor: "#ffffff",
            lineWidth: 1,
            medianWidth: 2,
            whiskerWidth: 2
        }, {
            pointArrayMap: ["low", "q1", "median", "q3", "high"],
            toYData: function(a) {
                return [a.low, a.q1, a.median, a.q3, a.high]
            },
            pointValKey: "high",
            pointAttribs: function() {
                return {}
            },
            drawDataLabels: w,
            translate: function() {
                var a = this.yAxis
                  , g = this.pointArrayMap;
                h.column.prototype.translate.apply(this);
                this.points.forEach(function(b) {
                    g.forEach(function(d) {
                        null !== b[d] && (b[d + "Plot"] = a.translate(b[d], 0, 1, 0, 1))
                    })
                })
            },
            drawPoints: function() {
                var a = this, h = a.options, b = a.chart, d = b.renderer, e, c, q, g, v, m, l = 0, n, f, k, C, y = !1 !== a.doQuartiles, B, F = a.options.whiskerLength;
                a.points.forEach(function(r) {
                    var t = r.graphic
                      , p = t ? "animate" : "attr"
                      , u = r.shapeArgs
                      , w = {}
                      , E = {}
                      , A = {}
                      , z = {}
                      , G = r.color || a.color;
                    void 0 !== r.plotY && (n = u.width,
                    f = Math.floor(u.x),
                    k = f + n,
                    C = Math.round(n / 2),
                    e = Math.floor(y ? r.q1Plot : r.lowPlot),
                    c = Math.floor(y ? r.q3Plot : r.lowPlot),
                    q = Math.floor(r.highPlot),
                    g = Math.floor(r.lowPlot),
                    t || (r.graphic = t = d.g("point").add(a.group),
                    r.stem = d.path().addClass("highcharts-boxplot-stem").add(t),
                    F && (r.whiskers = d.path().addClass("highcharts-boxplot-whisker").add(t)),
                    y && (r.box = d.path(void 0).addClass("highcharts-boxplot-box").add(t)),
                    r.medianShape = d.path(void 0).addClass("highcharts-boxplot-median").add(t)),
                    b.styledMode || (E.stroke = r.stemColor || h.stemColor || G,
                    E["stroke-width"] = x(r.stemWidth, h.stemWidth, h.lineWidth),
                    E.dashstyle = r.stemDashStyle || h.stemDashStyle,
                    r.stem.attr(E),
                    F && (A.stroke = r.whiskerColor || h.whiskerColor || G,
                    A["stroke-width"] = x(r.whiskerWidth, h.whiskerWidth, h.lineWidth),
                    r.whiskers.attr(A)),
                    y && (w.fill = r.fillColor || h.fillColor || G,
                    w.stroke = h.lineColor || G,
                    w["stroke-width"] = h.lineWidth || 0,
                    r.box.attr(w)),
                    z.stroke = r.medianColor || h.medianColor || G,
                    z["stroke-width"] = x(r.medianWidth, h.medianWidth, h.lineWidth),
                    r.medianShape.attr(z)),
                    m = r.stem.strokeWidth() % 2 / 2,
                    l = f + C + m,
                    r.stem[p]({
                        d: ["M", l, c, "L", l, q, "M", l, e, "L", l, g]
                    }),
                    y && (m = r.box.strokeWidth() % 2 / 2,
                    e = Math.floor(e) + m,
                    c = Math.floor(c) + m,
                    f += m,
                    k += m,
                    r.box[p]({
                        d: ["M", f, c, "L", f, e, "L", k, e, "L", k, c, "L", f, c, "z"]
                    })),
                    F && (m = r.whiskers.strokeWidth() % 2 / 2,
                    q += m,
                    g += m,
                    B = /%$/.test(F) ? C * parseFloat(F) / 100 : F / 2,
                    r.whiskers[p]({
                        d: ["M", l - B, q, "L", l + B, q, "M", l - B, g, "L", l + B, g]
                    })),
                    v = Math.round(r.medianPlot),
                    m = r.medianShape.strokeWidth() % 2 / 2,
                    v += m,
                    r.medianShape[p]({
                        d: ["M", f, v, "L", k, v]
                    }))
                })
            },
            setStackedPoints: w
        })
    }
    )(z);
    (function(a) {
        var w = a.noop
          , x = a.seriesType
          , g = a.seriesTypes;
        x("errorbar", "boxplot", {
            color: "#000000",
            grouping: !1,
            linkedTo: ":previous",
            tooltip: {
                pointFormat: '\x3cspan style\x3d"color:{point.color}"\x3e\u25cf\x3c/span\x3e {series.name}: \x3cb\x3e{point.low}\x3c/b\x3e - \x3cb\x3e{point.high}\x3c/b\x3e\x3cbr/\x3e'
            },
            whiskerWidth: null
        }, {
            type: "errorbar",
            pointArrayMap: ["low", "high"],
            toYData: function(a) {
                return [a.low, a.high]
            },
            pointValKey: "high",
            doQuartiles: !1,
            drawDataLabels: g.arearange ? function() {
                var a = this.pointValKey;
                g.arearange.prototype.drawDataLabels.call(this);
                this.data.forEach(function(h) {
                    h.y = h[a]
                })
            }
            : w,
            getColumnMetrics: function() {
                return this.linkedParent && this.linkedParent.columnMetrics || g.column.prototype.getColumnMetrics.call(this)
            }
        })
    }
    )(z);
    (function(a) {
        var w = a.correctFloat
          , x = a.isNumber
          , g = a.pick
          , h = a.objectEach
          , u = a.arrayMin
          , p = a.arrayMax
          , b = a.addEvent
          , d = a.Chart
          , e = a.Point
          , c = a.Series
          , q = a.seriesType
          , t = a.seriesTypes;
        b(a.Axis, "afterInit", function() {
            this.isXAxis || (this.waterfallStacks = {})
        });
        b(d, "beforeRedraw", function() {
            for (var a = this.axes, b = this.series, c = b.length; c--; )
                b[c].options.stacking && (a.forEach(function(a) {
                    a.isXAxis || (a.waterfallStacks = {})
                }),
                c = 0)
        });
        q("waterfall", "column", {
            dataLabels: {
                inside: !0
            },
            lineWidth: 1,
            lineColor: "#333333",
            dashStyle: "Dot",
            borderColor: "#333333",
            states: {
                hover: {
                    lineWidthPlus: 0
                }
            }
        }, {
            pointValKey: "y",
            showLine: !0,
            generatePoints: function() {
                var a, b, c, d;
                t.column.prototype.generatePoints.apply(this);
                c = 0;
                for (b = this.points.length; c < b; c++)
                    if (a = this.points[c],
                    d = this.processedYData[c],
                    a.isIntermediateSum || a.isSum)
                        a.y = w(d)
            },
            translate: function() {
                var a = this.options, b = this.yAxis, c, d, f, k, e, y, h, q, r, p = g(a.minPointLength, 5), u = p / 2, w = a.threshold, x = a.stacking, E = b.waterfallStacks[this.stackKey], A;
                t.column.prototype.translate.apply(this);
                h = q = w;
                d = this.points;
                c = 0;
                for (a = d.length; c < a; c++)
                    f = d[c],
                    y = this.processedYData[c],
                    k = f.shapeArgs,
                    r = [0, y],
                    A = f.y,
                    x ? E && (r = E[c],
                    "overlap" === x ? (e = r.threshold + r.total,
                    r.total -= A,
                    e = 0 <= A ? e : e - A) : 0 <= A ? (e = r.threshold + r.posTotal,
                    r.posTotal -= A) : (e = r.threshold + r.negTotal,
                    r.negTotal -= A,
                    e -= A),
                    f.isSum || (r.connectorThreshold = r.threshold + r.stackTotal),
                    b.reversed ? (y = 0 <= A ? e - A : e + A,
                    A = e) : (y = e,
                    A = e - A),
                    f.below = y <= g(w, 0),
                    k.y = b.translate(y, 0, 1, 0, 1),
                    k.height = Math.abs(k.y - b.translate(A, 0, 1, 0, 1))) : (e = Math.max(h, h + A) + r[0],
                    k.y = b.translate(e, 0, 1, 0, 1),
                    f.isSum ? (k.y = b.translate(r[1], 0, 1, 0, 1),
                    k.height = Math.min(b.translate(r[0], 0, 1, 0, 1), b.len) - k.y) : f.isIntermediateSum ? (0 <= A ? (y = r[1] + q,
                    A = q) : (y = q,
                    A = r[1] + q),
                    b.reversed && (y ^= A,
                    A ^= y,
                    y ^= A),
                    k.y = b.translate(y, 0, 1, 0, 1),
                    k.height = Math.abs(k.y - Math.min(b.translate(A, 0, 1, 0, 1), b.len)),
                    q += r[1]) : (k.height = 0 < y ? b.translate(h, 0, 1, 0, 1) - k.y : b.translate(h, 0, 1, 0, 1) - b.translate(h - y, 0, 1, 0, 1),
                    h += y,
                    f.below = h < g(w, 0)),
                    0 > k.height && (k.y += k.height,
                    k.height *= -1)),
                    f.plotY = k.y = Math.round(k.y) - this.borderWidth % 2 / 2,
                    k.height = Math.max(Math.round(k.height), .001),
                    f.yBottom = k.y + k.height,
                    k.height <= p && !f.isNull ? (k.height = p,
                    k.y -= u,
                    f.plotY = k.y,
                    f.minPointLengthOffset = 0 > f.y ? -u : u) : (f.isNull && (k.width = 0),
                    f.minPointLengthOffset = 0),
                    k = f.plotY + (f.negative ? k.height : 0),
                    this.chart.inverted ? f.tooltipPos[0] = b.len - k : f.tooltipPos[1] = k
            },
            processData: function(a) {
                var b = this.options, l = this.yData, d = b.data, f, k = l.length, e = b.threshold || 0, v, h, q, r, g, t;
                for (t = h = v = q = r = 0; t < k; t++)
                    g = l[t],
                    f = d && d[t] ? d[t] : {},
                    "sum" === g || f.isSum ? l[t] = w(h) : "intermediateSum" === g || f.isIntermediateSum ? (l[t] = w(v),
                    v = 0) : (h += g,
                    v += g),
                    q = Math.min(h, q),
                    r = Math.max(h, r);
                c.prototype.processData.call(this, a);
                b.stacking || (this.dataMin = q + e,
                this.dataMax = r)
            },
            toYData: function(a) {
                return a.isSum ? 0 === a.x ? null : "sum" : a.isIntermediateSum ? 0 === a.x ? null : "intermediateSum" : a.y
            },
            pointAttribs: function(a, b) {
                var c = this.options.upColor;
                c && !a.options.color && (a.color = 0 < a.y ? c : null);
                a = t.column.prototype.pointAttribs.call(this, a, b);
                delete a.dashstyle;
                return a
            },
            getGraphPath: function() {
                return ["M", 0, 0]
            },
            getCrispPath: function() {
                var a = this.data, b = this.yAxis, c = a.length, d = Math.round(this.graph.strokeWidth()) % 2 / 2, f = Math.round(this.borderWidth) % 2 / 2, k = this.xAxis.reversed, e = this.yAxis.reversed, h = this.options.stacking, q = [], g, r, t, p, u, w, x;
                for (w = 1; w < c; w++) {
                    u = a[w].shapeArgs;
                    r = a[w - 1];
                    p = a[w - 1].shapeArgs;
                    g = b.waterfallStacks[this.stackKey];
                    t = 0 < r.y ? -p.height : 0;
                    g && (g = g[w - 1],
                    h ? (g = g.connectorThreshold,
                    t = Math.round(b.translate(g, 0, 1, 0, 1) + (e ? t : 0)) - d) : t = p.y + r.minPointLengthOffset + f - d,
                    x = ["M", p.x + (k ? 0 : p.width), t, "L", u.x + (k ? u.width : 0), t]);
                    if (!h && 0 > r.y && !e || 0 < r.y && e)
                        x[2] += p.height,
                        x[5] += p.height;
                    q = q.concat(x)
                }
                return q
            },
            drawGraph: function() {
                c.prototype.drawGraph.call(this);
                this.graph.attr({
                    d: this.getCrispPath()
                })
            },
            setStackedPoints: function() {
                var a = this.options, b = this.yAxis.waterfallStacks, c = a.threshold, d = c || 0, f = c || 0, k = this.stackKey, e = this.xData, h = e.length, g, q, r, t;
                if (this.visible || !this.chart.options.chart.ignoreHiddenSeries)
                    for (b[k] || (b[k] = {}),
                    b = b[k],
                    k = 0; k < h; k++)
                        g = e[k],
                        b[g] || (b[g] = {
                            negTotal: 0,
                            posTotal: 0,
                            total: 0,
                            stackTotal: 0,
                            threshold: 0,
                            stackState: [d]
                        }),
                        g = b[g],
                        q = this.yData[k],
                        0 <= q ? g.posTotal += q : g.negTotal += q,
                        t = a.data[k],
                        q = g.posTotal,
                        r = g.negTotal,
                        t && t.isIntermediateSum ? (d ^= f,
                        f ^= d,
                        d ^= f) : t && t.isSum && (d = c),
                        g.stackTotal = q + r,
                        g.total = g.stackTotal,
                        g.threshold = d,
                        g.stackState[0] = d,
                        g.stackState.push(g.stackTotal),
                        d += g.stackTotal
            },
            getExtremes: function() {
                var a = this.options.stacking, b, c, d, f, k;
                a && (b = this.yAxis,
                b = b.waterfallStacks,
                c = this.stackedYNeg = [],
                d = this.stackedYPos = [],
                "overlap" === a ? h(b[this.stackKey], function(a) {
                    f = [];
                    a.stackState.forEach(function(b, c) {
                        k = a.stackState[0];
                        c ? f.push(b + k) : f.push(k)
                    });
                    c.push(u(f));
                    d.push(p(f))
                }) : h(b[this.stackKey], function(a) {
                    c.push(a.negTotal + a.threshold);
                    d.push(a.posTotal + a.threshold)
                }),
                this.dataMin = u(c),
                this.dataMax = p(d))
            }
        }, {
            getClassName: function() {
                var a = e.prototype.getClassName.call(this);
                this.isSum ? a += " highcharts-sum" : this.isIntermediateSum && (a += " highcharts-intermediate-sum");
                return a
            },
            isValid: function() {
                return x(this.y, !0) || this.isSum || this.isIntermediateSum
            }
        })
    }
    )(z);
    (function(a) {
        var w = a.Series
          , x = a.seriesType
          , g = a.seriesTypes;
        x("polygon", "scatter", {
            marker: {
                enabled: !1,
                states: {
                    hover: {
                        enabled: !1
                    }
                }
            },
            stickyTracking: !1,
            tooltip: {
                followPointer: !0,
                pointFormat: ""
            },
            trackByArea: !0
        }, {
            type: "polygon",
            getGraphPath: function() {
                for (var a = w.prototype.getGraphPath.call(this), g = a.length + 1; g--; )
                    (g === a.length || "M" === a[g]) && 0 < g && a.splice(g, 0, "z");
                return this.areaPath = a
            },
            drawGraph: function() {
                this.options.fillColor = this.color;
                g.area.prototype.drawGraph.call(this)
            },
            drawLegendSymbol: a.LegendSymbolMixin.drawRectangle,
            drawTracker: w.prototype.drawTracker,
            setStackedPoints: a.noop
        })
    }
    )(z);
    (function(a) {
        var w = a.Series
          , x = a.Legend
          , g = a.Chart
          , h = a.addEvent
          , u = a.wrap
          , p = a.color
          , b = a.isNumber
          , d = a.numberFormat
          , e = a.objectEach
          , c = a.merge
          , q = a.noop
          , t = a.pick
          , v = a.stableSort
          , m = a.setOptions
          , l = a.arrayMin
          , n = a.arrayMax;
        m({
            legend: {
                bubbleLegend: {
                    borderColor: void 0,
                    borderWidth: 2,
                    className: void 0,
                    color: void 0,
                    connectorClassName: void 0,
                    connectorColor: void 0,
                    connectorDistance: 60,
                    connectorWidth: 1,
                    enabled: !1,
                    labels: {
                        className: void 0,
                        allowOverlap: !1,
                        format: "",
                        formatter: void 0,
                        align: "right",
                        style: {
                            fontSize: 10,
                            color: void 0
                        },
                        x: 0,
                        y: 0
                    },
                    maxSize: 60,
                    minSize: 10,
                    legendIndex: 0,
                    ranges: {
                        value: void 0,
                        borderColor: void 0,
                        color: void 0,
                        connectorColor: void 0
                    },
                    sizeBy: "area",
                    sizeByAbsoluteValue: !1,
                    zIndex: 1,
                    zThreshold: 0
                }
            }
        });
        a.BubbleLegend = function(a, b) {
            this.init(a, b)
        }
        ;
        a.BubbleLegend.prototype = {
            init: function(a, b) {
                this.options = a;
                this.visible = !0;
                this.chart = b.chart;
                this.legend = b
            },
            setState: q,
            addToLegend: function(a) {
                a.splice(this.options.legendIndex, 0, this)
            },
            drawLegendSymbol: function(a) {
                var f = this.chart, c = this.options, d = t(a.options.itemDistance, 20), e, l = c.ranges;
                e = c.connectorDistance;
                this.fontMetrics = f.renderer.fontMetrics(c.labels.style.fontSize.toString() + "px");
                l && l.length && b(l[0].value) ? (v(l, function(a, b) {
                    return b.value - a.value
                }),
                this.ranges = l,
                this.setOptions(),
                this.render(),
                f = this.getMaxLabelSize(),
                l = this.ranges[0].radius,
                a = 2 * l,
                e = e - l + f.width,
                e = 0 < e ? e : 0,
                this.maxLabel = f,
                this.movementX = "left" === c.labels.align ? e : 0,
                this.legendItemWidth = a + e + d,
                this.legendItemHeight = a + this.fontMetrics.h / 2) : a.options.bubbleLegend.autoRanges = !0
            },
            setOptions: function() {
                var a = this
                  , b = a.ranges
                  , d = a.options
                  , e = a.chart.series[d.seriesIndex]
                  , l = a.legend.baseline
                  , g = {
                    "z-index": d.zIndex,
                    "stroke-width": d.borderWidth
                }
                  , m = {
                    "z-index": d.zIndex,
                    "stroke-width": d.connectorWidth
                }
                  , h = a.getLabelStyles()
                  , n = e.options.marker.fillOpacity
                  , q = a.chart.styledMode;
                b.forEach(function(f, k) {
                    q || (g.stroke = t(f.borderColor, d.borderColor, e.color),
                    g.fill = t(f.color, d.color, 1 !== n ? p(e.color).setOpacity(n).get("rgba") : e.color),
                    m.stroke = t(f.connectorColor, d.connectorColor, e.color));
                    b[k].radius = a.getRangeRadius(f.value);
                    b[k] = c(b[k], {
                        center: b[0].radius - b[k].radius + l
                    });
                    q || c(!0, b[k], {
                        bubbleStyle: c(!1, g),
                        connectorStyle: c(!1, m),
                        labelStyle: h
                    })
                })
            },
            getLabelStyles: function() {
                var a = this.options
                  , b = {}
                  , d = "left" === a.labels.align
                  , l = this.legend.options.rtl;
                e(a.labels.style, function(a, f) {
                    "color" !== f && "fontSize" !== f && "z-index" !== f && (b[f] = a)
                });
                return c(!1, b, {
                    "font-size": a.labels.style.fontSize,
                    fill: t(a.labels.style.color, "#000000"),
                    "z-index": a.zIndex,
                    align: l || d ? "right" : "left"
                })
            },
            getRangeRadius: function(a) {
                var b = this.options;
                return this.chart.series[this.options.seriesIndex].getRadius.call(this, b.ranges[b.ranges.length - 1].value, b.ranges[0].value, b.minSize, b.maxSize, a)
            },
            render: function() {
                var a = this
                  , b = a.chart.renderer
                  , c = a.options.zThreshold;
                a.symbols || (a.symbols = {
                    connectors: [],
                    bubbleItems: [],
                    labels: []
                });
                a.legendSymbol = b.g("bubble-legend");
                a.legendItem = b.g("bubble-legend-item");
                a.legendSymbol.translateX = 0;
                a.legendSymbol.translateY = 0;
                a.ranges.forEach(function(b) {
                    b.value >= c && a.renderRange(b)
                });
                a.legendSymbol.add(a.legendItem);
                a.legendItem.add(a.legendGroup);
                a.hideOverlappingLabels()
            },
            renderRange: function(a) {
                var b = this.options, c = b.labels, f = this.chart.renderer, d = this.symbols, e = d.labels, l = a.center, g = Math.abs(a.radius), m = b.connectorDistance, h = c.align, n = c.style.fontSize, m = this.legend.options.rtl || "left" === h ? -m : m, c = b.connectorWidth, q = this.ranges[0].radius, v = l - g - b.borderWidth / 2 + c / 2, t, n = n / 2 - (this.fontMetrics.h - n) / 2, p = f.styledMode;
                "center" === h && (m = 0,
                b.connectorDistance = 0,
                a.labelStyle.align = "center");
                h = v + b.labels.y;
                t = q + m + b.labels.x;
                d.bubbleItems.push(f.circle(q, l + ((v % 1 ? 1 : .5) - (c % 2 ? 0 : .5)), g).attr(p ? {} : a.bubbleStyle).addClass((p ? "highcharts-color-" + this.options.seriesIndex + " " : "") + "highcharts-bubble-legend-symbol " + (b.className || "")).add(this.legendSymbol));
                d.connectors.push(f.path(f.crispLine(["M", q, v, "L", q + m, v], b.connectorWidth)).attr(p ? {} : a.connectorStyle).addClass((p ? "highcharts-color-" + this.options.seriesIndex + " " : "") + "highcharts-bubble-legend-connectors " + (b.connectorClassName || "")).add(this.legendSymbol));
                a = f.text(this.formatLabel(a), t, h + n).attr(p ? {} : a.labelStyle).addClass("highcharts-bubble-legend-labels " + (b.labels.className || "")).add(this.legendSymbol);
                e.push(a);
                a.placed = !0;
                a.alignAttr = {
                    x: t,
                    y: h + n
                }
            },
            getMaxLabelSize: function() {
                var a, b;
                this.symbols.labels.forEach(function(c) {
                    b = c.getBBox(!0);
                    a = a ? b.width > a.width ? b : a : b
                });
                return a || {}
            },
            formatLabel: function(b) {
                var c = this.options
                  , f = c.labels.formatter;
                return (c = c.labels.format) ? a.format(c, b) : f ? f.call(b) : d(b.value, 1)
            },
            hideOverlappingLabels: function() {
                var a = this.chart
                  , b = this.symbols;
                !this.options.labels.allowOverlap && b && (a.hideOverlappingLabels(b.labels),
                b.labels.forEach(function(a, c) {
                    a.newOpacity ? a.newOpacity !== a.oldOpacity && b.connectors[c].show() : b.connectors[c].hide()
                }))
            },
            getRanges: function() {
                var a = this.legend.bubbleLegend, k, d = a.options.ranges, e, g = Number.MAX_VALUE, m = -Number.MAX_VALUE;
                a.chart.series.forEach(function(a) {
                    a.isBubble && !a.ignoreSeries && (e = a.zData.filter(b),
                    e.length && (g = t(a.options.zMin, Math.min(g, Math.max(l(e), !1 === a.options.displayNegative ? a.options.zThreshold : -Number.MAX_VALUE))),
                    m = t(a.options.zMax, Math.max(m, n(e)))))
                });
                k = g === m ? [{
                    value: m
                }] : [{
                    value: g
                }, {
                    value: (g + m) / 2
                }, {
                    value: m,
                    autoRanges: !0
                }];
                d.length && d[0].radius && k.reverse();
                k.forEach(function(a, b) {
                    d && d[b] && (k[b] = c(!1, d[b], a))
                });
                return k
            },
            predictBubbleSizes: function() {
                var a = this.chart
                  , b = this.fontMetrics
                  , c = a.legend.options
                  , d = "horizontal" === c.layout
                  , e = d ? a.legend.lastLineHeight : 0
                  , l = a.plotSizeX
                  , g = a.plotSizeY
                  , m = a.series[this.options.seriesIndex]
                  , a = Math.ceil(m.minPxSize)
                  , h = Math.ceil(m.maxPxSize)
                  , m = m.options.maxSize
                  , n = Math.min(g, l);
                if (c.floating || !/%$/.test(m))
                    b = h;
                else if (m = parseFloat(m),
                b = (n + e - b.h / 2) * m / 100 / (m / 100 + 1),
                d && g - b >= l || !d && l - b >= g)
                    b = h;
                return [a, Math.ceil(b)]
            },
            updateRanges: function(a, b) {
                var c = this.legend.options.bubbleLegend;
                c.minSize = a;
                c.maxSize = b;
                c.ranges = this.getRanges()
            },
            correctSizes: function() {
                var a = this.legend
                  , b = this.chart.series[this.options.seriesIndex];
                1 < Math.abs(Math.ceil(b.maxPxSize) - this.options.maxSize) && (this.updateRanges(this.options.minSize, b.maxPxSize),
                a.render())
            }
        };
        h(a.Legend, "afterGetAllItems", function(b) {
            var c = this.bubbleLegend
              , f = this.options
              , d = f.bubbleLegend
              , e = this.chart.getVisibleBubbleSeriesIndex();
            c && c.ranges && c.ranges.length && (d.ranges.length && (d.autoRanges = !!d.ranges[0].autoRanges),
            this.destroyItem(c));
            0 <= e && f.enabled && d.enabled && (d.seriesIndex = e,
            this.bubbleLegend = new a.BubbleLegend(d,this),
            this.bubbleLegend.addToLegend(b.allItems))
        });
        g.prototype.getVisibleBubbleSeriesIndex = function() {
            for (var a = this.series, b = 0; b < a.length; ) {
                if (a[b] && a[b].isBubble && a[b].visible && a[b].zData.length)
                    return b;
                b++
            }
            return -1
        }
        ;
        x.prototype.getLinesHeights = function() {
            var a = this.allItems, b = [], c, d = a.length, e, l = 0;
            for (e = 0; e < d; e++)
                if (a[e].legendItemHeight && (a[e].itemHeight = a[e].legendItemHeight),
                a[e] === a[d - 1] || a[e + 1] && a[e]._legendItemPos[1] !== a[e + 1]._legendItemPos[1]) {
                    b.push({
                        height: 0
                    });
                    c = b[b.length - 1];
                    for (l; l <= e; l++)
                        a[l].itemHeight > c.height && (c.height = a[l].itemHeight);
                    c.step = e
                }
            return b
        }
        ;
        x.prototype.retranslateItems = function(a) {
            var b, c, d, f = this.options.rtl, e = 0;
            this.allItems.forEach(function(l, k) {
                b = l.legendGroup.translateX;
                c = l._legendItemPos[1];
                if ((d = l.movementX) || f && l.ranges)
                    d = f ? b - l.options.maxSize / 2 : b + d,
                    l.legendGroup.attr({
                        translateX: d
                    });
                k > a[e].step && e++;
                l.legendGroup.attr({
                    translateY: Math.round(c + a[e].height / 2)
                });
                l._legendItemPos[1] = c + a[e].height / 2
            })
        }
        ;
        h(w, "legendItemClick", function() {
            var a = this.chart
              , b = this.visible
              , c = this.chart.legend;
            c && c.bubbleLegend && (this.visible = !b,
            this.ignoreSeries = b,
            a = 0 <= a.getVisibleBubbleSeriesIndex(),
            c.bubbleLegend.visible !== a && (c.update({
                bubbleLegend: {
                    enabled: a
                }
            }),
            c.bubbleLegend.visible = a),
            this.visible = b)
        });
        u(g.prototype, "drawChartBox", function(a, b, c) {
            var d = this.legend, f = 0 <= this.getVisibleBubbleSeriesIndex(), l;
            d && d.options.enabled && d.bubbleLegend && d.options.bubbleLegend.autoRanges && f ? (l = d.bubbleLegend.options,
            f = d.bubbleLegend.predictBubbleSizes(),
            d.bubbleLegend.updateRanges(f[0], f[1]),
            l.placed || (d.group.placed = !1,
            d.allItems.forEach(function(a) {
                a.legendGroup.translateY = null
            })),
            d.render(),
            this.getMargins(),
            this.axes.forEach(function(a) {
                a.render();
                l.placed || (a.setScale(),
                a.updateNames(),
                e(a.ticks, function(a) {
                    a.isNew = !0;
                    a.isNewLabel = !0
                }))
            }),
            l.placed = !0,
            this.getMargins(),
            a.call(this, b, c),
            d.bubbleLegend.correctSizes(),
            d.retranslateItems(d.getLinesHeights())) : (a.call(this, b, c),
            d && d.options.enabled && d.bubbleLegend && (d.render(),
            d.retranslateItems(d.getLinesHeights())))
        })
    }
    )(z);
    (function(a) {
        var w = a.arrayMax
          , x = a.arrayMin
          , g = a.Axis
          , h = a.color
          , u = a.isNumber
          , p = a.noop
          , b = a.pick
          , d = a.pInt
          , e = a.Point
          , c = a.Series
          , q = a.seriesType
          , t = a.seriesTypes;
        q("bubble", "scatter", {
            dataLabels: {
                formatter: function() {
                    return this.point.z
                },
                inside: !0,
                verticalAlign: "middle"
            },
            animationLimit: 250,
            marker: {
                lineColor: null,
                lineWidth: 1,
                fillOpacity: .5,
                radius: null,
                states: {
                    hover: {
                        radiusPlus: 0
                    }
                },
                symbol: "circle"
            },
            minSize: 8,
            maxSize: "20%",
            softThreshold: !1,
            states: {
                hover: {
                    halo: {
                        size: 5
                    }
                }
            },
            tooltip: {
                pointFormat: "({point.x}, {point.y}), Size: {point.z}"
            },
            turboThreshold: 0,
            zThreshold: 0,
            zoneAxis: "z"
        }, {
            pointArrayMap: ["y", "z"],
            parallelArrays: ["x", "y", "z"],
            trackerGroups: ["group", "dataLabelsGroup"],
            specialGroup: "group",
            bubblePadding: !0,
            zoneAxis: "z",
            directTouch: !0,
            isBubble: !0,
            pointAttribs: function(a, b) {
                var d = this.options.marker.fillOpacity;
                a = c.prototype.pointAttribs.call(this, a, b);
                1 !== d && (a.fill = h(a.fill).setOpacity(d).get("rgba"));
                return a
            },
            getRadii: function(a, b, c) {
                var d, f = this.zData, e = c.minPxSize, l = c.maxPxSize, m = [], g;
                d = 0;
                for (c = f.length; d < c; d++)
                    g = f[d],
                    m.push(this.getRadius(a, b, e, l, g));
                this.radii = m
            },
            getRadius: function(a, b, c, d, f) {
                var e = this.options
                  , l = "width" !== e.sizeBy
                  , g = e.zThreshold
                  , m = b - a;
                e.sizeByAbsoluteValue && null !== f && (f = Math.abs(f - g),
                m = Math.max(b - g, Math.abs(a - g)),
                a = 0);
                u(f) ? f < a ? c = c / 2 - 1 : (a = 0 < m ? (f - a) / m : .5,
                l && 0 <= a && (a = Math.sqrt(a)),
                c = Math.ceil(c + a * (d - c)) / 2) : c = null;
                return c
            },
            animate: function(a) {
                !a && this.points.length < this.options.animationLimit && (this.points.forEach(function(a) {
                    var b = a.graphic, c;
                    b && b.width && (c = {
                        x: b.x,
                        y: b.y,
                        width: b.width,
                        height: b.height
                    },
                    b.attr({
                        x: a.plotX,
                        y: a.plotY,
                        width: 1,
                        height: 1
                    }),
                    b.animate(c, this.options.animation))
                }, this),
                this.animate = null)
            },
            translate: function() {
                var b, c = this.data, d, e, f = this.radii;
                t.scatter.prototype.translate.call(this);
                for (b = c.length; b--; )
                    d = c[b],
                    e = f ? f[b] : 0,
                    u(e) && e >= this.minPxSize / 2 ? (d.marker = a.extend(d.marker, {
                        radius: e,
                        width: 2 * e,
                        height: 2 * e
                    }),
                    d.dlBox = {
                        x: d.plotX - e,
                        y: d.plotY - e,
                        width: 2 * e,
                        height: 2 * e
                    }) : d.shapeArgs = d.plotY = d.dlBox = void 0
            },
            alignDataLabel: t.column.prototype.alignDataLabel,
            buildKDTree: p,
            applyZones: p
        }, {
            haloPath: function(a) {
                return e.prototype.haloPath.call(this, 0 === a ? 0 : (this.marker ? this.marker.radius || 0 : 0) + a)
            },
            ttBelow: !1
        });
        g.prototype.beforePadding = function() {
            var c = this
              , e = this.len
              , g = this.chart
              , h = 0
              , f = e
              , k = this.isXAxis
              , q = k ? "xData" : "yData"
              , t = this.min
              , p = {}
              , z = Math.min(g.plotWidth, g.plotHeight)
              , r = Number.MAX_VALUE
              , I = -Number.MAX_VALUE
              , J = this.max - t
              , H = e / J
              , D = [];
            this.series.forEach(function(e) {
                var f = e.options;
                !e.bubblePadding || !e.visible && g.options.chart.ignoreHiddenSeries || (c.allowZoomOutside = !0,
                D.push(e),
                k && (["minSize", "maxSize"].forEach(function(a) {
                    var b = f[a]
                      , c = /%$/.test(b)
                      , b = d(b);
                    p[a] = c ? z * b / 100 : b
                }),
                e.minPxSize = p.minSize,
                e.maxPxSize = Math.max(p.maxSize, p.minSize),
                e = e.zData.filter(a.isNumber),
                e.length && (r = b(f.zMin, Math.min(r, Math.max(x(e), !1 === f.displayNegative ? f.zThreshold : -Number.MAX_VALUE))),
                I = b(f.zMax, Math.max(I, w(e))))))
            });
            D.forEach(function(a) {
                var b = a[q], d = b.length, e;
                k && a.getRadii(r, I, a);
                if (0 < J)
                    for (; d--; )
                        u(b[d]) && c.dataMin <= b[d] && b[d] <= c.dataMax && (e = a.radii[d],
                        h = Math.min((b[d] - t) * H - e, h),
                        f = Math.max((b[d] - t) * H + e, f))
            });
            D.length && 0 < J && !this.isLog && (f -= e,
            H *= (e + Math.max(0, h) - Math.min(f, e)) / e,
            [["min", "userMin", h], ["max", "userMax", f]].forEach(function(a) {
                void 0 === b(c.options[a[0]], c[a[1]]) && (c[a[0]] += a[2] / H)
            }))
        }
    }
    )(z);
    (function(a) {
        var w = a.seriesType
          , x = a.defined;
        w("packedbubble", "bubble", {
            minSize: "10%",
            maxSize: "100%",
            sizeBy: "radius",
            zoneAxis: "y",
            tooltip: {
                pointFormat: "Value: {point.value}"
            }
        }, {
            pointArrayMap: ["value"],
            pointValKey: "value",
            isCartesian: !1,
            axisTypes: [],
            accumulateAllPoints: function(a) {
                var g = a.chart, u = [], p, b;
                for (p = 0; p < g.series.length; p++)
                    if (a = g.series[p],
                    a.visible || !g.options.chart.ignoreHiddenSeries)
                        for (b = 0; b < a.yData.length; b++)
                            u.push([null, null, a.yData[b], a.index, b]);
                return u
            },
            translate: function() {
                var g, h = this.chart, u = this.data, p = this.index, b, d, e;
                this.processedXData = this.xData;
                this.generatePoints();
                x(h.allDataPoints) || (h.allDataPoints = this.accumulateAllPoints(this),
                this.getPointRadius());
                g = this.placeBubbles(h.allDataPoints);
                for (e = 0; e < g.length; e++)
                    g[e][3] === p && (b = u[g[e][4]],
                    d = g[e][2],
                    b.plotX = g[e][0] - h.plotLeft + h.diffX,
                    b.plotY = g[e][1] - h.plotTop + h.diffY,
                    b.marker = a.extend(b.marker, {
                        radius: d,
                        width: 2 * d,
                        height: 2 * d
                    }))
            },
            checkOverlap: function(a, h) {
                var g = a[0] - h[0]
                  , p = a[1] - h[1];
                return -.001 > Math.sqrt(g * g + p * p) - Math.abs(a[2] + h[2])
            },
            positionBubble: function(a, h, u) {
                var g = Math.sqrt
                  , b = Math.asin
                  , d = Math.acos
                  , e = Math.pow
                  , c = Math.abs
                  , g = g(e(a[0] - h[0], 2) + e(a[1] - h[1], 2))
                  , d = d((e(g, 2) + e(u[2] + h[2], 2) - e(u[2] + a[2], 2)) / (2 * (u[2] + h[2]) * g))
                  , b = b(c(a[0] - h[0]) / g);
                a = (0 > a[1] - h[1] ? 0 : Math.PI) + d + b * (0 > (a[0] - h[0]) * (a[1] - h[1]) ? 1 : -1);
                return [h[0] + (h[2] + u[2]) * Math.sin(a), h[1] - (h[2] + u[2]) * Math.cos(a), u[2], u[3], u[4]]
            },
            placeBubbles: function(a) {
                var g = this.checkOverlap, u = this.positionBubble, p = [], b = 1, d = 0, e = 0, c, q;
                c = a.sort(function(a, b) {
                    return b[2] - a[2]
                });
                if (!c.length)
                    return [];
                if (2 > c.length)
                    return [0, 0, c[0][0], c[0][1], c[0][2]];
                p.push([[0, 0, c[0][2], c[0][3], c[0][4]]]);
                p.push([[0, 0 - c[1][2] - c[0][2], c[1][2], c[1][3], c[1][4]]]);
                for (q = 2; q < c.length; q++)
                    c[q][2] = c[q][2] || 1,
                    a = u(p[b][d], p[b - 1][e], c[q]),
                    g(a, p[b][0]) ? (p.push([]),
                    e = 0,
                    p[b + 1].push(u(p[b][d], p[b][0], c[q])),
                    b++,
                    d = 0) : 1 < b && p[b - 1][e + 1] && g(a, p[b - 1][e + 1]) ? (e++,
                    p[b].push(u(p[b][d], p[b - 1][e], c[q])),
                    d++) : (d++,
                    p[b].push(a));
                this.chart.stages = p;
                this.chart.rawPositions = [].concat.apply([], p);
                this.resizeRadius();
                return this.chart.rawPositions
            },
            resizeRadius: function() {
                var a = this.chart, h = a.rawPositions, u = Math.min, p = Math.max, b = a.plotLeft, d = a.plotTop, e = a.plotHeight, c = a.plotWidth, q, t, v, m, l, n;
                q = v = Number.POSITIVE_INFINITY;
                t = m = Number.NEGATIVE_INFINITY;
                for (n = 0; n < h.length; n++)
                    l = h[n][2],
                    q = u(q, h[n][0] - l),
                    t = p(t, h[n][0] + l),
                    v = u(v, h[n][1] - l),
                    m = p(m, h[n][1] + l);
                n = [t - q, m - v];
                u = u.apply([], [(c - b) / n[0], (e - d) / n[1]]);
                if (1e-10 < Math.abs(u - 1)) {
                    for (n = 0; n < h.length; n++)
                        h[n][2] *= u;
                    this.placeBubbles(h)
                } else
                    a.diffY = e / 2 + d - v - (m - v) / 2,
                    a.diffX = c / 2 + b - q - (t - q) / 2
            },
            getPointRadius: function() {
                var a = this, h = a.chart, u = a.options, p = Math.min(h.plotWidth, h.plotHeight), b = {}, d = [], e = h.allDataPoints, c, q, t, v;
                ["minSize", "maxSize"].forEach(function(a) {
                    var c = parseInt(u[a], 10)
                      , d = /%$/.test(c);
                    b[a] = d ? p * c / 100 : c
                });
                h.minRadius = c = b.minSize;
                h.maxRadius = q = b.maxSize;
                (e || []).forEach(function(b, l) {
                    t = b[2];
                    v = a.getRadius(c, q, c, q, t);
                    0 === t && (v = null);
                    e[l][2] = v;
                    d.push(v)
                });
                this.radii = d
            },
            alignDataLabel: a.Series.prototype.alignDataLabel
        });
        a.addEvent(a.seriesTypes.packedbubble, "updatedData", function() {
            var a = this;
            this.chart.series.forEach(function(g) {
                g.type === a.type && (g.isDirty = !0)
            })
        });
        a.addEvent(a.Chart, "beforeRedraw", function() {
            this.allDataPoints && delete this.allDataPoints
        })
    }
    )(z);
    (function(a) {
        var w = a.pick
          , x = a.Series
          , g = a.seriesTypes
          , h = a.wrap
          , u = x.prototype
          , p = a.Pointer.prototype;
        a.polarExtended || (a.polarExtended = !0,
        u.searchPointByAngle = function(a) {
            var b = this.chart
              , e = this.xAxis.pane.center;
            return this.searchKDTree({
                clientX: 180 + -180 / Math.PI * Math.atan2(a.chartX - e[0] - b.plotLeft, a.chartY - e[1] - b.plotTop)
            })
        }
        ,
        u.getConnectors = function(a, d, e, c) {
            var b, g, h, m, l, n, f, k;
            g = c ? 1 : 0;
            b = 0 <= d && d <= a.length - 1 ? d : 0 > d ? a.length - 1 + d : 0;
            d = 0 > b - 1 ? a.length - (1 + g) : b - 1;
            g = b + 1 > a.length - 1 ? g : b + 1;
            h = a[d];
            g = a[g];
            m = h.plotX;
            h = h.plotY;
            l = g.plotX;
            n = g.plotY;
            g = a[b].plotX;
            b = a[b].plotY;
            m = (1.5 * g + m) / 2.5;
            h = (1.5 * b + h) / 2.5;
            l = (1.5 * g + l) / 2.5;
            f = (1.5 * b + n) / 2.5;
            n = Math.sqrt(Math.pow(m - g, 2) + Math.pow(h - b, 2));
            k = Math.sqrt(Math.pow(l - g, 2) + Math.pow(f - b, 2));
            m = Math.atan2(h - b, m - g);
            f = Math.PI / 2 + (m + Math.atan2(f - b, l - g)) / 2;
            Math.abs(m - f) > Math.PI / 2 && (f -= Math.PI);
            m = g + Math.cos(f) * n;
            h = b + Math.sin(f) * n;
            l = g + Math.cos(Math.PI + f) * k;
            f = b + Math.sin(Math.PI + f) * k;
            g = {
                rightContX: l,
                rightContY: f,
                leftContX: m,
                leftContY: h,
                plotX: g,
                plotY: b
            };
            e && (g.prevPointCont = this.getConnectors(a, d, !1, c));
            return g
        }
        ,
        u.toXY = function(a) {
            var b, e = this.chart, c = a.plotX;
            b = a.plotY;
            a.rectPlotX = c;
            a.rectPlotY = b;
            b = this.xAxis.postTranslate(a.plotX, this.yAxis.len - b);
            a.plotX = a.polarPlotX = b.x - e.plotLeft;
            a.plotY = a.polarPlotY = b.y - e.plotTop;
            this.kdByAngle ? (e = (c / Math.PI * 180 + this.xAxis.pane.options.startAngle) % 360,
            0 > e && (e += 360),
            a.clientX = e) : a.clientX = a.plotX
        }
        ,
        g.spline && (h(g.spline.prototype, "getPointSpline", function(a, d, e, c) {
            this.chart.polar ? c ? (a = this.getConnectors(d, c, !0, this.connectEnds),
            a = ["C", a.prevPointCont.rightContX, a.prevPointCont.rightContY, a.leftContX, a.leftContY, a.plotX, a.plotY]) : a = ["M", e.plotX, e.plotY] : a = a.call(this, d, e, c);
            return a
        }),
        g.areasplinerange && (g.areasplinerange.prototype.getPointSpline = g.spline.prototype.getPointSpline)),
        a.addEvent(x, "afterTranslate", function() {
            var b = this.chart, d, e;
            if (b.polar) {
                (this.kdByAngle = b.tooltip && b.tooltip.shared) ? this.searchPoint = this.searchPointByAngle : this.options.findNearestPointBy = "xy";
                if (!this.preventPostTranslate)
                    for (d = this.points,
                    e = d.length; e--; )
                        this.toXY(d[e]);
                this.hasClipCircleSetter || (this.hasClipCircleSetter = !!a.addEvent(this, "afterRender", function() {
                    var c;
                    b.polar && (c = this.yAxis.center,
                    this.group.clip(b.renderer.clipCircle(c[0], c[1], c[2] / 2)),
                    this.setClip = a.noop)
                }))
            }
        }, {
            order: 2
        }),
        h(u, "getGraphPath", function(a, d) {
            var b = this, c, g, h;
            if (this.chart.polar) {
                d = d || this.points;
                for (c = 0; c < d.length; c++)
                    if (!d[c].isNull) {
                        g = c;
                        break
                    }
                !1 !== this.options.connectEnds && void 0 !== g && (this.connectEnds = !0,
                d.splice(d.length, 0, d[g]),
                h = !0);
                d.forEach(function(a) {
                    void 0 === a.polarPlotY && b.toXY(a)
                })
            }
            c = a.apply(this, [].slice.call(arguments, 1));
            h && d.pop();
            return c
        }),
        x = function(a, d) {
            var b = this.chart
              , c = this.options.animation
              , g = this.group
              , h = this.markerGroup
              , p = this.xAxis.center
              , m = b.plotLeft
              , l = b.plotTop;
            b.polar ? b.renderer.isSVG && (!0 === c && (c = {}),
            d ? (a = {
                translateX: p[0] + m,
                translateY: p[1] + l,
                scaleX: .001,
                scaleY: .001
            },
            g.attr(a),
            h && h.attr(a)) : (a = {
                translateX: m,
                translateY: l,
                scaleX: 1,
                scaleY: 1
            },
            g.animate(a, c),
            h && h.animate(a, c),
            this.animate = null)) : a.call(this, d)
        }
        ,
        h(u, "animate", x),
        g.column && (g = g.column.prototype,
        g.polarArc = function(a, d, e, c) {
            var b = this.xAxis.center
              , g = this.yAxis.len;
            return this.chart.renderer.symbols.arc(b[0], b[1], g - d, null, {
                start: e,
                end: c,
                innerR: g - w(a, g)
            })
        }
        ,
        h(g, "animate", x),
        h(g, "translate", function(a) {
            var b = this.xAxis, e = b.startAngleRad, c, g, h;
            this.preventPostTranslate = !0;
            a.call(this);
            if (b.isRadial)
                for (c = this.points,
                h = c.length; h--; )
                    g = c[h],
                    a = g.barX + e,
                    g.shapeType = "path",
                    g.shapeArgs = {
                        d: this.polarArc(g.yBottom, g.plotY, a, a + g.pointWidth)
                    },
                    this.toXY(g),
                    g.tooltipPos = [g.plotX, g.plotY],
                    g.ttBelow = g.plotY > b.center[1]
        }),
        h(g, "alignDataLabel", function(a, d, e, c, g, h) {
            this.chart.polar ? (a = d.rectPlotX / Math.PI * 180,
            null === c.align && (c.align = 20 < a && 160 > a ? "left" : 200 < a && 340 > a ? "right" : "center"),
            null === c.verticalAlign && (c.verticalAlign = 45 > a || 315 < a ? "bottom" : 135 < a && 225 > a ? "top" : "middle"),
            u.alignDataLabel.call(this, d, e, c, g, h)) : a.call(this, d, e, c, g, h)
        })),
        h(p, "getCoordinates", function(a, d) {
            var b = this.chart
              , c = {
                xAxis: [],
                yAxis: []
            };
            b.polar ? b.axes.forEach(function(a) {
                var e = a.isXAxis
                  , g = a.center
                  , h = d.chartX - g[0] - b.plotLeft
                  , g = d.chartY - g[1] - b.plotTop;
                c[e ? "xAxis" : "yAxis"].push({
                    axis: a,
                    value: a.translate(e ? Math.PI - Math.atan2(h, g) : Math.sqrt(Math.pow(h, 2) + Math.pow(g, 2)), !0)
                })
            }) : c = a.call(this, d);
            return c
        }),
        a.SVGRenderer.prototype.clipCircle = function(b, d, e) {
            var c = a.uniqueKey()
              , g = this.createElement("clipPath").attr({
                id: c
            }).add(this.defs);
            b = this.circle(b, d, e).add(g);
            b.id = c;
            b.clipPath = g;
            return b
        }
        ,
        a.addEvent(a.Chart, "getAxes", function() {
            this.pane || (this.pane = []);
            a.splat(this.options.pane).forEach(function(b) {
                new a.Pane(b,this)
            }, this)
        }),
        a.addEvent(a.Chart, "afterDrawChartBox", function() {
            this.pane.forEach(function(a) {
                a.render()
            })
        }),
        h(a.Chart.prototype, "get", function(b, d) {
            return a.find(this.pane, function(a) {
                return a.options.id === d
            }) || b.call(this, d)
        }))
    }
    )(z)
});
//# sourceMappingURL=highcharts-more.js.map
