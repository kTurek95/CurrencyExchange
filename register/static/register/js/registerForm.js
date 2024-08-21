const registerButton = document.querySelector('.register-button')
const registerForm = document.querySelectorAll('.register-input')
const formDivs = document.querySelectorAll('form div')
const password1Input = document.querySelector('#id_password1')
const password2Input = document.querySelector('#id_password2')
const myModal = document.querySelector('.modal')



const checkIfFieldIsNotEmpty = () =>
{
    let isValid=true
    for (let i=0; i<registerForm.length; i++)
    {
       for (let j=0; j<formDivs.length; j++)
       {
           if (i === j)
           {
               let existingError = formDivs[j].querySelector(`.error-${formDivs[j].id}`);
                if (existingError) {
                    existingError.remove();
                }
               if (registerForm[i].value === '')
               {
                   let existingError = document.querySelector(`.error-${formDivs[j].id}`)
                   if (!existingError)
                   {
                       const errorP = document.createElement('p')
                       errorP.setAttribute('class', `error-${formDivs[j].id}`)
                       errorP.innerText = `${registerForm[i].name} cannot be empty`
                       errorP.style.color = 'red'
                       errorP.style.marginLeft = '5px'
                       formDivs[j].appendChild(errorP)
                   }
                   isValid = false
               }
           }

       }
    }
    return isValid;
}


const checkIfPasswordsMatch = (e) =>
{
    if (password1Input.value !== password2Input.value)
    {
        e.preventDefault();
        myModal.style.display = 'block'
        const modalButton = document.querySelector('#modal-button')
        modalButton.addEventListener('click', () =>
    {
        myModal.style.display = 'none'
    })

    }
}

registerButton.addEventListener('click', (event) =>
{
    const isValid = checkIfFieldIsNotEmpty()

    if (!isValid)
    {
        event.preventDefault();
    }

    checkIfPasswordsMatch(event)
});



