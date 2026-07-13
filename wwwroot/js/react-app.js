document.addEventListener('DOMContentLoaded', function () {
    const rootElement = document.getElementById('react-root');
    if (!rootElement) {
        return;
    }

    const e = React.createElement;

    function Counter() {
        const [count, setCount] = React.useState(0);
        return e(
            'div',
            { className: 'card mx-auto', style: { maxWidth: '420px' } },
            e('div', { className: 'card-body' },
                e('h2', { className: 'card-title' }, 'React Counter'),
                e('p', { className: 'card-text' }, 'This part of the page is rendered with React.'),
                e('div', { className: 'd-flex align-items-center justify-content-between' },
                    e('button', {
                        className: 'btn btn-primary',
                        onClick: () => setCount(count - 1)
                    }, '-'),
                    e('span', { className: 'fs-4 mb-0' }, count),
                    e('button', {
                        className: 'btn btn-primary',
                        onClick: () => setCount(count + 1)
                    }, '+')
                )
            )
        );
    }

    if (ReactDOM.createRoot) {
        ReactDOM.createRoot(rootElement).render(e(Counter));
    } else {
        ReactDOM.render(e(Counter), rootElement);
    }
});
