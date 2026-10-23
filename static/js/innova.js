/* Prix SJI Innova : comportements et animations */
(function () {
    'use strict';
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var $ = function (s, c) {
        return (c || document).querySelector(s);
    };
    var $$ = function (s, c) {
        return Array.prototype.slice.call((c || document).querySelectorAll(s));
    };

    /* 1. En-tête : ombre au défilement */
    var header = $('.site-header');
    if (header) {
        var onScroll = function () {
            header.classList.toggle('scrolled', window.scrollY > 8);
        };
        window.addEventListener('scroll', onScroll, {passive: true});
        onScroll();
    }

    /* 2. Titres : apparition mot par mot */
    $$('[data-split]').forEach(function (el) {
        var text = el.textContent.trim().replace(/\s+/g, ' ');
        var words = text.split(' ');
        el.setAttribute('aria-label', text);
        el.textContent = '';
        words.forEach(function (w, i) {
            var outer = document.createElement('span');
            var inner = document.createElement('span');
            outer.className = 'sw';
            outer.setAttribute('aria-hidden', 'true');
            inner.textContent = w;
            inner.style.setProperty('--i', i);
            outer.appendChild(inner);
            el.appendChild(outer);
            if (i < words.length - 1) el.appendChild(document.createTextNode(' '));
        });
        requestAnimationFrame(function () {
            requestAnimationFrame(function () {
                el.classList.add('split-ready');
            });
        });
    });

    /* 3. Compteurs */
    function count(el) {
        var to = parseFloat(el.getAttribute('data-count')) || 0;
        if (reduce) {
            el.textContent = to;
            return;
        }
        var t0 = performance.now(), dur = 1300;
        (function step(t) {
            var p = Math.min(1, (t - t0) / dur);
            el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
            if (p < 1) requestAnimationFrame(step);
        })(t0);
    }

    /* 4. Révélations au défilement */
    $$('[data-stagger]').forEach(function (parent) {
        var step = parseInt(parent.getAttribute('data-stagger'), 10) || 90;
        Array.prototype.forEach.call(parent.children, function (child, i) {
            if (!child.hasAttribute('data-reveal')) child.setAttribute('data-reveal', '');
            child.style.setProperty('--d', i * step);
        });
    });
    $$('[data-reveal]').forEach(function (el) {
        if (el.dataset.delay && !el.style.getPropertyValue('--d')) el.style.setProperty('--d', el.dataset.delay);
    });
    var targets = $$('[data-reveal],[data-anim]');

    function show(el) {
        el.classList.add('in');
        $$('[data-count]', el).forEach(count);
    }

    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                if (e.isIntersecting) {
                    show(e.target);
                    io.unobserve(e.target);
                }
            });
        }, {threshold: 0.12, rootMargin: '0px 0px -5% 0px'});
        targets.forEach(function (el) {
            io.observe(el);
        });
    } else {
        targets.forEach(show);
    }

    /* 5. Logo : léger effet de profondeur à la souris */
    var bp = $('.blueprint');
    if (bp && !reduce && window.matchMedia('(pointer: fine)').matches) {
        bp.addEventListener('mousemove', function (e) {
            var r = bp.getBoundingClientRect();
            bp.style.setProperty('--px', ((e.clientX - r.left) / r.width - 0.5) * 16 + 'px');
            bp.style.setProperty('--py', ((e.clientY - r.top) / r.height - 0.5) * 16 + 'px');
        });
        bp.addEventListener('mouseleave', function () {
            bp.style.setProperty('--px', '0px');
            bp.style.setProperty('--py', '0px');
        });
    }

    /* 6. Messages : fermeture automatique des confirmations */
    $$('.flash[data-autohide]').forEach(function (el) {
        var ms = parseInt(el.getAttribute('data-autohide'), 10) || 7000;
        setTimeout(function () {
            if (document.body.contains(el) && window.bootstrap) bootstrap.Alert.getOrCreateInstance(el).close();
        }, ms);
    });

    /* 7. Formulaires : état d’envoi, focus sur les erreurs */
    $$('form').forEach(function (f) {
        f.addEventListener('submit', function (e) {
            if (f.dataset.sent) {
                e.preventDefault();
                return;
            }
            var b = e.submitter || $('button[type=submit]', f);
            if (!b || b.hasAttribute('data-no-loading')) return;
            f.dataset.sent = '1';
            setTimeout(function () {
                b.classList.add('is-loading');
                b.setAttribute('aria-busy', 'true');
            }, 0);
        });
    });
    window.addEventListener('pageshow', function (e) {
        if (!e.persisted) return;
        $$('form').forEach(function (f) {
            delete f.dataset.sent;
        });
        $$('.btn.is-loading').forEach(function (b) {
            b.classList.remove('is-loading');
            b.removeAttribute('aria-busy');
        });
    });
    var formAlert = $('.form-alert');
    if (formAlert) {
        setTimeout(function () {
            formAlert.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'});
            formAlert.focus({preventScroll: true});
        }, 200);
    }
    $$('a[data-focus]').forEach(function (a) {
        a.addEventListener('click', function (e) {
            var t = document.getElementById(a.getAttribute('href').slice(1));
            if (!t) return;
            e.preventDefault();
            t.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block: 'center'});
            t.focus({preventScroll: true});
        });
    });

    /* 8. Filtres : envoi automatique des listes déroulantes */
    $$('form[data-filters]').forEach(function (f) {
        $$('select', f).forEach(function (s) {
            s.addEventListener('change', function () {
                f.requestSubmit ? f.requestSubmit() : f.submit();
            });
        });
    });

    /* 9. Modale de confirmation (actions sensibles en POST) */
    var cm = document.getElementById('confirmModal');
    if (cm && window.bootstrap) {
        var modal = bootstrap.Modal.getOrCreateInstance(cm);
        var confirmForm = $('#confirmForm', cm);
        var pending = null;
        $$('[data-confirm]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var ownForm = btn.closest('form');
                pending = (!btn.dataset.action && ownForm) ? {form: ownForm, btn: btn} : null;
                confirmForm.setAttribute('action', btn.dataset.action || '');
                $('#confirmTitle', cm).textContent = btn.dataset.title || 'Confirmer cette action ?';
                $('#confirmText', cm).textContent = btn.dataset.text || '';
                $('#confirmOk', cm).textContent = btn.dataset.ok || 'Confirmer';
                $('#confirmOk', cm).disabled = false;
                modal.show();
            });
        });
        confirmForm.addEventListener('submit', function (e) {
            if (!pending) return;               /* mode « la modale poste elle-même » */
            e.preventDefault();
            var p = pending;
            pending = null;
            if (p.btn.name) {
                var h = document.createElement('input');
                h.type = 'hidden';
                h.name = p.btn.name;
                h.value = p.btn.value;
                p.form.appendChild(h);
            }
            $('#confirmOk', cm).disabled = true;   /* évite un double clic */
            p.form.submit();                    /* envoie le formulaire d’origine */
        });
    }

    /* 10. Modale de détails (contenu masqué dans la page) */
    var dm = document.getElementById('detailModal');
    if (dm && window.bootstrap) {
        var dmodal = bootstrap.Modal.getOrCreateInstance(dm);
        $$('[data-detail]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var src = $(btn.dataset.detail);
                if (!src) return;
                $('#detailTitle', dm).textContent = btn.dataset.title || 'Détails';
                $('#detailBody', dm).innerHTML = src.innerHTML;
                dmodal.show();
            });
        });
    }
})();



