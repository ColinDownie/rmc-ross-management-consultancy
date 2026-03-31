/* ----------------------------------------------------------
   Ross Consultancy Group – Unified Router
   Centralised URL mapping for all divisions
---------------------------------------------------------- */

const ROSS_ROUTES = {
    rpc: "https://yourusername.github.io/ross-property-consultancy/",
    rmc: "https://yourusername.github.io/rmc-ross-management-consultancy/",
    rcc: "https://yourusername.github.io/rcc-ross-creative-consultancy/",
    rsc: "https://yourusername.github.io/rsc-ross-strategy-consultancy/",
    group: "https://yourusername.github.io/ross-consultancy-group/"
};

window.RossRouter = {
    go(div) {
        if (ROSS_ROUTES[div]) {
            window.location.href = ROSS_ROUTES[div];
        } else {
            console.warn("Unknown division:", div);
        }
    },
    list() {
        console.table(ROSS_ROUTES);
    }
};
