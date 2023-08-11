import { computed } from 'vue';
import { BarcodeScanner } from '@capacitor-community/barcode-scanner';
import { useQuasar } from 'quasar';
import { useToast } from 'vue-toastification';
import { ClientError } from 'graphql-request'

import { useAuthStore } from 'src/stores/auth';
import { useUserStore } from 'src/stores/user';
import { useUser } from 'src/composables';
import { CompanyUser, User } from 'src/types/user';

export function useScanner(addPatient: boolean) {
  const authStore = useAuthStore()
  const userStore = useUserStore()
  const { getUserById, createAuthorizationPendency } = useUser()
  const $q = useQuasar()
  const toast = useToast()
  const userProfile = computed(() => authStore.user)

  const hideBackground = () => {
    document.body.style.opacity = '0';
    document.body.style.background = 'transparent';
    BarcodeScanner.hideBackground();
  };

  const confirmAddPatient = (patient: User) => {
    $q.dialog({
      title: 'Confirm',
      message: `Do you confirm add ${patient.name} as your patient?`,
      cancel: true,
      persistent: true,
    }).onOk(async () => {
      try {
        const groupId = patient.groups?.edges ? patient.groups.edges[0].node?.id : 2
        const user: CompanyUser = {
          companyId: userProfile.value?.company?.id,
          userId: patient.id,
          doctorId: userProfile.value?.id,
          groupId,
          approvalById: userProfile.value?.id,
          requestedById: patient.id,
          status: 'Approve',
          joinedDatetime: new Date().toISOString(),
          approvalAt: new Date().toISOString(),
          isOwner: false,
          isActive: false,
        }
        await createAuthorizationPendency(user)
        toast.success(`Success! You have now access to ${patient.name} records. Use the platform page to manage the access.`);
      } catch (error: unknown) {
        handleError(error)
      }
    });
  };

  const scanNewPatient = async () => {
    const result = await BarcodeScanner.startScan();
    if (result.hasContent) {
      document.body.style.background = '';
      document.body.style.opacity = '1';

      try {
        let userId = 0
        if (result.content) {
          userId = parseInt(result.content)
        }
        await getUserById(userId)
        if (userStore.user) {
          confirmAddPatient(userStore.user);
        }
      } catch (error: unknown) {
        handleError(error)
      }
    }
  };

  const scanNewManagedPatient = async () => {
    const result = await BarcodeScanner.startScan();
    if (result.hasContent) {
      document.body.style.background = '';
      document.body.style.opacity = '1';

      try {
        //
      } catch (error: unknown) {
        handleError(error)
      }
    }
  };

  const startScan = async () => {
    hideBackground();
    if (process.env.DEV) {
      console.log('starting scan...');
    }


    const status = await BarcodeScanner.checkPermission({ force: true });

    if (status.granted) {
      addPatient ? scanNewPatient() : scanNewManagedPatient();
    }
  };

  const handleError = (error: unknown) => {
    if (process.env.DEV) {
      console.error(JSON.stringify(error, undefined, 2))
    }
    if (error instanceof ClientError) {
      error.response.errors?.forEach(e => toast.error(e.message))
    } else {
      toast.error('Something went wrong, please try again later')
    }
  }

  return { startScan };
};
