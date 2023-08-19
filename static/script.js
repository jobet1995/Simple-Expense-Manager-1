const showExpenseFormButton = document.getElementById('showExpenseForm');
const contentDiv = document.getElementById('content');

showExpenseFormButton.addEventListener('click', () => {
  // Change the URL hash to "expense-form"
  window.location.hash = 'expense-form';
});

// Check the hash when the page loads
window.addEventListener('load', () => {
  if (window.location.hash === '#expense-form') {
    loadComponent('ExpenseForm.html');
  }
});

function loadComponent(componentFile) {
  contentDiv.innerHTML = ''; // Clear previous content
  fetch(componentFile)
    .then(response => response.text())
    .then(html => {
      contentDiv.innerHTML = html;

      if (componentFile === 'ExpenseForm.html') {
        const addButton = document.getElementById('addButton');

        addButton.addEventListener('click', () => {
          const descriptionInput = document.getElementById('description');
          const amountInput = document.getElementById('amount');
          const description = descriptionInput.value;
          const amount = parseFloat(amountInput.value);
          const currentDate = new Date().toISOString().split('T')[0];

          if (description && amount) {
            const newExpense = { description, amount, date: currentDate };

            // Handle the form submission and adding expense here
            fetch('/api/expenses', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(newExpense)
            })
              .then(response => response.json())
              .then(data => {
                console.log('Expense added:', data.message);
                // Optionally, you can reload the Expense List component here
              })
              .catch(error => {
                console.error('Error adding expense:', error);
              });
          }
        });
      }
    });
}
