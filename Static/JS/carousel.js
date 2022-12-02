function carousel_toConsumableArray(arr) { return carousel_arrayWithoutHoles(arr) || carousel_iterableToArray(arr) || carousel_unsupportedIterableToArray(arr) || carousel_nonIterableSpread(); }

function carousel_nonIterableSpread() { throw new TypeError("Invalid attempt to spread non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); }

function carousel_unsupportedIterableToArray(o, minLen) { if (!o) return; if (typeof o === "string") return carousel_arrayLikeToArray(o, minLen); var n = Object.prototype.toString.call(o).slice(8, -1); if (n === "Object" && o.constructor) n = o.constructor.name; if (n === "Map" || n === "Set") return Array.from(o); if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return carousel_arrayLikeToArray(o, minLen); }

function carousel_iterableToArray(iter) { if (typeof Symbol !== "undefined" && iter[Symbol.iterator] != null || iter["@@iterator"] != null) return Array.from(iter); }

function carousel_arrayWithoutHoles(arr) { if (Array.isArray(arr)) return carousel_arrayLikeToArray(arr); }

function carousel_arrayLikeToArray(arr, len) { if (len == null || len > arr.length) len = arr.length; for (var i = 0, arr2 = new Array(len); i < len; i++) { arr2[i] = arr[i]; } return arr2; }

function carousel_ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); enumerableOnly && (symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; })), keys.push.apply(keys, symbols); } return keys; }

function carousel_objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = null != arguments[i] ? arguments[i] : {}; i % 2 ? carousel_ownKeys(Object(source), !0).forEach(function (key) { carousel_defineProperty(target, key, source[key]); }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)) : carousel_ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } return target; }

function carousel_defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

function carousel_classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function carousel_defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function carousel_createClass(Constructor, protoProps, staticProps) { if (protoProps) carousel_defineProperties(Constructor.prototype, protoProps); if (staticProps) carousel_defineProperties(Constructor, staticProps); Object.defineProperty(Constructor, "prototype", { writable: false }); return Constructor; }

var carousel_Default = {
    defaultPosition: 0,
    indicators: {
        items: [],
        activeClasses: 'bg-white dark:bg-gray-800',
        inactiveClasses: 'bg-white/50 dark:bg-gray-800/50 hover:bg-white dark:hover:bg-gray-800'
    },
    interval: 3000,
    onNext: function onNext() { },
    onPrev: function onPrev() { },
    onChange: function onChange() { }
};

var Carousel = /*#__PURE__*/function () {
    function Carousel() {
        var items = arguments.length > 0 && arguments[0] !== undefined ? arguments[0] : [];
        var options = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {};

        carousel_classCallCheck(this, Carousel);

        this._items = items;
        this._options = carousel_objectSpread(carousel_objectSpread(carousel_objectSpread({}, carousel_Default), options), {}, {
            indicators: carousel_objectSpread(carousel_objectSpread({}, carousel_Default.indicators), options.indicators)
        });
        this._activeItem = this.getItem(this._options.defaultPosition);
        this._indicators = this._options.indicators.items;
        this._interval = null;

        this._init();
    }
    /**
     * Initialise carousel and items based on active one
     */


    carousel_createClass(Carousel, [{
        key: "_init",
        value: function _init() {
            var _this = this;

            this._items.map(function (item) {
                item.el.classList.add('absolute', 'inset-0', 'transition-all', 'transform');
            }); // if no active item is set then first position is default


            if (this._getActiveItem()) {
                this.slideTo(this._getActiveItem().position);
            } else {
                this.slideTo(0);
            }

            this._indicators.map(function (indicator, position) {
                indicator.el.addEventListener('click', function () {
                    _this.slideTo(position);
                });
            });
        }
    }, {
        key: "getItem",
        value: function getItem(position) {
            return this._items[position];
        }
        /**
         * Slide to the element based on id
         * @param {*} position 
         */

    }, {
        key: "slideTo",
        value: function slideTo(position) {
            var nextItem = this._items[position];
            var rotationItems = {
                'left': nextItem.position === 0 ? this._items[this._items.length - 1] : this._items[nextItem.position - 1],
                'middle': nextItem,
                'right': nextItem.position === this._items.length - 1 ? this._items[0] : this._items[nextItem.position + 1]
            };

            this._rotate(rotationItems);

            this._setActiveItem(nextItem.position);

            if (this._interval) {
                this.pause();
                this.cycle();
            }

            this._options.onChange(this);
        }
        /**
         * Based on the currently active item it will go to the next position
         */

    }, {
        key: "next",
        value: function next() {
            var activeItem = this._getActiveItem();

            var nextItem = null; // check if last item

            if (activeItem.position === this._items.length - 1) {
                nextItem = this._items[0];
            } else {
                nextItem = this._items[activeItem.position + 1];
            }

            this.slideTo(nextItem.position); // callback function

            this._options.onNext(this);
        }
        /**
         * Based on the currently active item it will go to the previous position
         */

    }, {
        key: "prev",
        value: function prev() {
            var activeItem = this._getActiveItem();

            var prevItem = null; // check if first item

            if (activeItem.position === 0) {
                prevItem = this._items[this._items.length - 1];
            } else {
                prevItem = this._items[activeItem.position - 1];
            }

            this.slideTo(prevItem.position); // callback function

            this._options.onPrev(this);
        }
        /**
         * This method applies the transform classes based on the left, middle, and right rotation carousel items
         * @param {*} rotationItems 
         */

    }, {
        key: "_rotate",
        value: function _rotate(rotationItems) {
            // reset
            this._items.map(function (item) {
                item.el.classList.add('hidden');
            }); // left item (previously active)


            rotationItems.left.el.classList.remove('-translate-x-full', 'translate-x-full', 'translate-x-0', 'hidden', 'z-20');
            rotationItems.left.el.classList.add('-translate-x-full', 'z-10'); // currently active item

            rotationItems.middle.el.classList.remove('-translate-x-full', 'translate-x-full', 'translate-x-0', 'hidden', 'z-10');
            rotationItems.middle.el.classList.add('translate-x-0', 'z-20'); // right item (upcoming active)

            rotationItems.right.el.classList.remove('-translate-x-full', 'translate-x-full', 'translate-x-0', 'hidden', 'z-20');
            rotationItems.right.el.classList.add('translate-x-full', 'z-10');
        }
        /**
         * Set an interval to cycle through the carousel items
         */

    }, {
        key: "cycle",
        value: function cycle() {
            var _this2 = this;

            this._interval = setInterval(function () {
                _this2.next();
            }, this._options.interval);
        }
        /**
         * Clears the cycling interval
         */

    }, {
        key: "pause",
        value: function pause() {
            clearInterval(this._interval);
        }
        /**
         * Get the currently active item
         */

    }, {
        key: "_getActiveItem",
        value: function _getActiveItem() {
            return this._activeItem;
        }
        /**
         * Set the currently active item and data attribute
         * @param {*} position 
         */

    }, {
        key: "_setActiveItem",
        value: function _setActiveItem(position) {
            var _this3 = this;

            this._activeItem = this._items[position]; // update the indicators if available

            if (this._indicators.length) {
                var _this$_indicators$pos, _this$_indicators$pos2;

                this._indicators.map(function (indicator) {
                    var _indicator$el$classLi, _indicator$el$classLi2;

                    indicator.el.setAttribute('aria-current', 'false');

                    (_indicator$el$classLi = indicator.el.classList).remove.apply(_indicator$el$classLi, carousel_toConsumableArray(_this3._options.indicators.activeClasses.split(" ")));

                    (_indicator$el$classLi2 = indicator.el.classList).add.apply(_indicator$el$classLi2, carousel_toConsumableArray(_this3._options.indicators.inactiveClasses.split(" ")));
                });

                (_this$_indicators$pos = this._indicators[position].el.classList).add.apply(_this$_indicators$pos, carousel_toConsumableArray(this._options.indicators.activeClasses.split(" ")));

                (_this$_indicators$pos2 = this._indicators[position].el.classList).remove.apply(_this$_indicators$pos2, carousel_toConsumableArray(this._options.indicators.inactiveClasses.split(" ")));

                this._indicators[position].el.setAttribute('aria-current', 'true');
            }
        }
    }]);

    return Carousel;
}();

window.Carousel = Carousel;

function initCarousel() {
    document.querySelectorAll('[data-carousel]').forEach(function (carouselEl) {
        var interval = carouselEl.getAttribute('data-carousel-interval');
        var slide = carouselEl.getAttribute('data-carousel') === 'slide' ? true : false;
        var items = [];
        var defaultPosition = 0;

        if (carouselEl.querySelectorAll('[data-carousel-item]').length) {
            carousel_toConsumableArray(carouselEl.querySelectorAll('[data-carousel-item]')).map(function (carouselItemEl, position) {
                items.push({
                    position: position,
                    el: carouselItemEl
                });

                if (carouselItemEl.getAttribute('data-carousel-item') === 'active') {
                    defaultPosition = position;
                }
            });
        }

        var indicators = [];

        if (carouselEl.querySelectorAll('[data-carousel-slide-to]').length) {
            carousel_toConsumableArray(carouselEl.querySelectorAll('[data-carousel-slide-to]')).map(function (indicatorEl) {
                indicators.push({
                    position: indicatorEl.getAttribute('data-carousel-slide-to'),
                    el: indicatorEl
                });
            });
        }

        var carousel = new Carousel(items, {
            defaultPosition: defaultPosition,
            indicators: {
                items: indicators
            },
            interval: interval ? interval : carousel_Default.interval
        });

        if (slide) {
            carousel.cycle();
        } // check for controls


        var carouselNextEl = carouselEl.querySelector('[data-carousel-next]');
        var carouselPrevEl = carouselEl.querySelector('[data-carousel-prev]');

        if (carouselNextEl) {
            carouselNextEl.addEventListener('click', function () {
                carousel.next();
            });
        }

        if (carouselPrevEl) {
            carouselPrevEl.addEventListener('click', function () {
                carousel.prev();
            });
        }
    });
}

if (document.readyState !== 'loading') {
    // DOMContentLoaded event were already fired. Perform explicit initialization now
    initCarousel();
} else {
    // DOMContentLoaded event not yet fired, attach initialization process to it
    document.addEventListener('DOMContentLoaded', initCarousel);
}

/* harmony default export */ const carousel = (Carousel);