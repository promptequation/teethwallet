import Vue from 'vue'
export default () => {
    Vue.directive('can', (el, binding, vnode) => {
        const behaviour = binding.modifiers.disable ? 'disable' : 'hide';
        let hasPermission = false
        if (binding.value) {
            hasPermission = true;
        } else {
            hasPermission = false;
        }
        if (!hasPermission) {
            if (behaviour === 'hide') {
                commentNode(el, vnode);
            } else if (behaviour === 'disable') {
                el.disabled = true;
            }
        }
    });
};

/**
 * Create comment node
 *
 */
function commentNode(el, vnode) {
    const comment = document.createComment(' ');

    Object.defineProperty(comment, 'setAttribute', {
        value: () => undefined,
    });

    vnode.text = ' ';
    vnode.elm = comment;
    vnode.isComment = true;
    vnode.context = undefined;
    vnode.tag = undefined;
    vnode.data.directives = undefined;

    if (vnode.componentInstance) {
        vnode.componentInstance.$el = comment;
    }

    if (el.parentNode) {
        el.parentNode.replaceChild(comment, el);
    }
}